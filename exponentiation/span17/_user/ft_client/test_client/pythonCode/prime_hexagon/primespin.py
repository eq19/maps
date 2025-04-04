"""  The Number Coil  """
#  List a prime; List mod6 of prime; Compare with another set (offset of mod6)
#  to see spin change, determine cell of each prime.
#
#

"""  This code plots the positons in the central triangle of the prime hexagon.

See accompanying notes and images for what these mean.

"""

import sys, os, glob
import logging
import re
import itertools

from collections import namedtuple

import numpy as np
import primesieve

_HAS_PRIMESIEVE_NUMPY = False
try:
    import primesieve.numpy
    _HAS_PRIMESIEVE_NUMPY = True
except:
    pass

_HAS_CYTHON_PRIMEHEX = False
try:
    import primehexagon
    _HAS_CYTHON_PRIMEHEX = True
except:
    pass

# python 2/3 compatibility stuff
try:
    l = long(1)
except:
    long = int

try:
    # python2 version of zip iterator is in itertools
    zipper = itertools.izip
except:
    # new python3 version is no longer in itertools. seriously?
    zipper = zip

logger = None
log_formatter = None

def setup_loggers():

    global logger, log_formatter
    if logger is not None:
        return
    
    # create logger
    logger = logging.getLogger('prime_hexagon')
    logger.setLevel(logging.INFO)

    # create formatter
    log_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

setup_loggers()

def list_generate_primes_array(a,b):
    logger.info("starting generating primes from {} to {}".format(a,b))
    logger.info("\tusing primesieve list prime generation")
    a = primesieve.primes(a,b)
    logger.info("\tprimes generated")
    a = np.array(a,dtype=np.uint64)
    logger.info("\toutput array created")
    logger.info("done generating primes")
    return a

def numpy_generate_primes_array(a,b):
    logger.info("starting generating primes from {} to {}".format(a,b))
    logger.info("\tusing numpy prime generator")
    import primesieve.numpy
    a = primesieve.numpy.primes(a,b)
    a = a.astype(np.uint64)
    logger.info("done generating primes")
    return a

def get_primes_generator():
    logger.info("selecting primes generation function")
    func = None
    if _HAS_PRIMESIEVE_NUMPY:
        logger.info("\tusing numpy prime generation...")
        func = numpy_generate_primes_array
    else:
        logger.info("\tfalling back to list primesieve prime generation")
        func = list_generate_primes_array

    logger.info("prime generator selected")
    return func


def _compute_spins(primes, last_prime, last_spin):
    """Returns array of SPINS given an array of PRIMES (assumed to be 1d)

    SPINS result array is same shape as PRIMES, with values stored in SPINS[1:]; 
    SPINS[0] = 0, use that zero element to thread chunked computations together.
    """
    
    logger.info("compute_spins: generating mod6Values")
    m6val  = primes % 6
    m6_offset_sum     = np.empty_like(primes, dtype=np.int32)
    m6_offset_sum[0]  = m6val[0] + (last_prime % 6)            #  seed value from current val + prev m6val
    m6_offset_sum[1:] = m6val[1:] + m6val[:-1]                 #  cur m6val + prev m6val
    logger.info("compute_spins: done mod6Values")
    logger.info("compute_spins: m6_off_sum={}".format(m6_offset_sum))

    logger.info("compute_spins: starting to compute spins")

    z = np.zeros_like(primes, dtype=np.int32)
    z[ m6_offset_sum ==  6] =  1
    z[ m6_offset_sum == 10] = -1
    z[ m6_offset_sum ==  2] = -1
    logger.info("compute_spins: z before last_spin={}".format(z))
    z[0] *= last_spin
    logger.info("compute_spins: z={}".format(z))
    spin = np.cumprod(z)

    logger.info("compute_spins: spin={}".format(spin))
    logger.info("compute_spins: done computing spins")
    return spin

def _compute_positions(spin, seed_pos, seed_spin):
    """Given an array of SPINS and two SEED_POSITION and SEED_SPIN values, compute the positions along the prime hex 

    """

    logger.info("compute_positions: starting aux calculations")
    delta = np.zeros_like(spin)
    delta[0]  = spin[0] - seed_spin      # first delta is cur_spin - prev_spin from seed_spin
    delta[1:] = spin[1:] - spin[:-1]     # delta is cur_spin - prev_spin 
    logger.info("compute_positions: delta={}".format(delta))

    #increments = np.copy(spin)           # copy the spin array,
    increments = np.abs(spin)           # copy the spin array,
    increments[ delta != 0 ] = 0          # set any non-zero delta to zero in the increment array
    logger.info("compute_positions: increments={}".format(increments))

    logger.info("compute_positions:\tdone with aux calculations")
    
    logger.info("compute_positions: starting primary calculation")

    # start at seed, cumulative add
    positions = np.copy(increments)
    #increments[0] = seed_pos
    outpositions = (seed_pos + np.cumsum(increments)) % 6
    logger.info("compute_positions: outpositions={}".format(outpositions))
    logger.info("compute_positions:\tdone with primary calculation")
    return outpositions


def _compute_rotations(positions, pos_seed, rot_seed ):

    logger.info("compute_rotations: starting aux calculations")
    #logger.info("positions array {}".format(positions))
    #logger.debug("rot_seed = {}".format(rot_seed))
    #logger.debug("pos_seed = {}".format(pos_seed))

    delta = np.zeros_like(positions)
    delta[1:] = positions[1:] - positions[:-1]
    delta[0] = positions[0] - pos_seed
    #logger.debug("delta array {}".format(delta))

    z = np.zeros_like(delta)       # zero array like delta
    z[ delta == -5 ] =  1          # where delta = -5, set increment to 1
    z[ delta ==  5 ] = -1          # where delta is 5, set increment to -1

    logger.info("compute_rotations: done with aux calculations")

    logger.info("compute_rotations: starting primary calculations")
    z[0] += rot_seed
    r = np.cumsum( z )
    
    logger.info("compute_rotations: done with primary calculations")

    return r

class PrimeSpinFuncs:
    def __init__(self, **opts):
        self.compute_spins     = opts.get('compute_spins',_compute_spins)
        self.compute_positions = opts.get('compute_positions',_compute_positions)
        self.compute_rotations = opts.get('compute_rotations',_compute_rotations)
        self.generate_primes   = opts.get('generate_primes')
        
_engines = {}
_engines['numpy'] = PrimeSpinFuncs(compute_spins = _compute_spins,
                                   compute_positions = _compute_positions,
                                   compute_rotations = _compute_rotations)

if _HAS_CYTHON_PRIMEHEX:
    _engines['cython'] = PrimeSpinFuncs(compute_spins = primehexagon._compute_spins,
                                        compute_positions = primehexagon._compute_positions,
                                        compute_rotations = primehexagon._compute_rotations)
    
## TODO: figure if we can generalize/refactor these array savers methods
def save_text_arrays( filename, data, save_opts):
    logger.info("start saving text results to file {0}".format(filename))

    skip_interval = save_opts.get('skip_interval',1)
    if skip_interval == 0:
        s = slice(-1,None,None)
    else:
        s = slice(None, None, skip_interval)

    logger.info("start zipping and slicing data together")
    outdata    = zipper(data.prime[s], data.pos[s], data.spin[s], data.rot[s])
    logger.info("\tdone zipping and slicing data")

    with open(filename, "w") as fp:
        w = fp.write
        # write each line as comma separated values
        sep = ','
        newline = '\n'
        for d in outdata:
            line = sep.join(map(str,d))
            w(line)
            w(newline)
    logger.info("done saving text file")
    
def save_binary_arrays( filename, data, save_opts):

    skip_interval = save_opts.get('skip_interval', 1)
    if skip_interval == 0:
        s = slice(-1, None,None)           # only take last value
    else:
        s = slice(None, None, skip_interval)

    do_compress = save_opts.get('compress', 1)
        
    if do_compress:
        (saver, msg) = (np.savez_compressed, "compressed")
    else:
        (saver, msg) = (np.savez,"uncompressed")
        
    logger.info("start save binary arrays {} to file {} with slice {}".format(msg, filename, s))
    saver(filename, prime=data.prime[s], spin=data.spin[s], pos=data.pos[s], rot=data.rot[s])
    logger.info("\tdone save binary arrays")


def compute_hex_positions(start, end, boundary_vals, save_opts):

    logger.info("save_opts is {}".format(save_opts))
    logger.info("boundary values are {}".format(boundary_vals))

    engine_name = save_opts.get('engine')
    engine = _engines.get(engine_name)
    if engine is None:
        raise ValueError("No hex position engine available for engine_name {}".format(engine_name))

    logger.info("using {} engine for computing hex positions".format(engine_name))

    if engine.generate_primes is None:
        engine.generate_primes = get_primes_generator()
        
    primes = engine.generate_primes(start, end)
    logger.info("type of primes array: {}".format(primes.dtype))
    
    # 2 and 3 are special, don't use them (they are the first two values, slice them out)
    if start < 2:
        primes = primes[2:]
    
    # 1 as last prime and last_spin and last_pos arespecial cases to start off the computation
    spin = engine.compute_spins(primes, boundary_vals.prime, boundary_vals.spin)
    pos  = engine.compute_positions(spin, boundary_vals.pos, boundary_vals.spin)
    rot  = engine.compute_rotations(pos, boundary_vals.pos, boundary_vals.rot)

    data = HexValues(primes, pos, spin, rot)
    new_hex_file = HexDataFile.save_new_file(start, end, data, save_opts)
    return new_hex_file

def _require_infile(infile):
    # we have a starting file, figure some stuff out
    if not os.path.isfile(infile):
        raise IOError("required input file {} does not exist".format(infile))

_VERBOSE = 5
def dprint(level, *args):
    if _VERBOSE >= level:
        logger.info(*args)

_HEX_FILENAME_RE = re.compile(r"-(?P<start>\d+)-(?P<end>\d+)(-(?P<skip>\d+))?.(?P<ext>(npz|txt))")
        
class HexDataAssets:
    def __init__(self, opts):
        self.basedir = opts.get('dir','output')
        self.basename = opts.get('basename','output')
        self._files = None

    @classmethod
    def get_hex_assets(klass, opts = None):
        if opts is None:
            basedir = 'data'
            basename = 'output'
        else:
            basedir = opts.dir or 'data'
            basename = opts.basename or 'output'
        h = klass(basedir, basename)
        return h

    def _clear_file_cache(self):
        self._files = None
    
    def list_files(self):
        # check cache
        if self._files:
            return files
        dprint(1, "looking for files in {}".format(self.basedir))
        files = os.listdir(self.basedir)
        filenames = [ os.path.join(self.basedir,f) for f in files if _HEX_FILENAME_RE.search(f) ]
        filenames.sort()
        dprint(1, "found {} files".format(len(filenames)))
        self._files = filenames
        return filenames
    
    def _find_files(self, vals, hex_predicate):
        """Return a SET of any files that contain any of the values specified"""
        s = set()
        for f in self.list_files():
            h = HexDataFile(f)
            dprint(2,"inspecting file {} for values {}".format(h, vals))
            if hex_predicate(h, vals):
                dprint(2,"\tsaving file for values {}".format(h, vals))
                s.add(h)
        return s

    def find_values_in_hexfiles(self, vals):
        hexfiles = self.find_files_with_values(vals)
        if not hexfiles:
            print("no files found containing the value {} in directory {}".format(vals, basedir))
            return None

        did_find = False
        for hfile in hexfiles:
            # stupid check to see if any of the values are in this file.
            indexes = hfile.values_around(vals)
            if indexes:
                print("file {}".format(hfile.filename))
            else:
                next
            # now figure out which values are in this file...
            for v in vals:
                indexes = hfile.values_around((v,))
                if indexes:
                    dprint(2, "found values in file {}".format(hfile))
                for idx in indexes:
                    did_find = True
                    # TODO: get it if primes are in the previous or next file
                    #  i.e. if idx-2 < 0, get primes from previous files
                    #       if idx+2 > length, get primes from next file
                    low = max(0, idx-1)
                    hi  = min( hfile.length(), idx+1)
                    dprint(2,"for val={} found index={} with low={}, hi={}".format(v, idx, low, hi))

                    data = hfile.get_sliced_zipped_arrays_iterator(slice(low,idx))
                    for d in data:
                        s = ','.join( map(str,d) ) 
                        sys.stdout.write(s + '\n')
                        
                        ##write_collection_to_file(sys.stdout, data)

                    print('----> {} <----'.format(v))

                    zipped_arrays = hfile.get_zipped_arrays_iterator()
                    data = hfile.get_sliced_zipped_arrays_iterator(slice(idx, hi))
                    for d in data:
                        s = ','.join( map(str,d) ) 
                        sys.stdout.write(s + '\n')

                    print("")
            return did_find
        
    def find_files_with_values(self, vals):
        """Return a SET of any files that contain any of the values specified"""
        return self._find_files(vals, HexDataFile.contains_any_values)
        s = set()
        for f in self.list_files():
            h = HexDataFile(f)
            dprint(2,"inspecting file {} for values {}".format(h, vals))
            if h.contains_any_values(vals):
                dprint(2,"\tsaving file for values {}".format(h, vals))
                s.add(h)
        return s
    
    def find_file_with_value(self, val):
        """Return a SET of any files that contain the value VAL"""
        return self._find_files(vals, HexDataFile.contains)
        s = set()
        for f in self.list_files():
            h = HexDataFile(f)
            dprint(2,"inspecting file {} for val {}".format(h, val))
            if h.contains(val):
                dprint(2,"\tsaving file {} for value {}".format(h, val))
                s.add(h)
        return s

    def compute_next_chunks(self, startFile, nvalues, nchunks, save_opts):
        hexFile = startFile
        start_val = hexFile.end
        for i in range(nchunks):
            end_val   = start_val + nvalues
            linkedValues = hexFile.get_last_values()
            new_hexfile = compute_hex_positions(start_val, end_val, linkedValues, save_opts)
            start_val = end_val
            hexFile = new_hexfile
        self._clear_file_cache()
        
    def compute_initial_chunks(self, nvalues, nchunks, save_opts):
        linkedValues = HexValues(1,1,1,0) # magic starting "previous" values
        hfile = compute_hex_positions(0, nvalues, linkedValues, save_opts)
        logger.info("save info: {}".format(save_opts))
        self.compute_next_chunks(hfile, nvalues, nchunks - 1, save_opts)

    def compute_provisional_chunks(self, start_value, nvalues, nchunks, save_opts):
        logger.info("computing provisional chunks, starting from {}".format(start_value))
        next_prime = primesieve.generate_n_primes(1, start_value)
        logger.info("next_prime for start_value={} is {}".format(start_value, next_prime))
        m6_start = next_prime[0] % 6
        logger.info("m6_start is {}".format(m6_start))
        if (m6_start == 1):
            logger.info("m6_start is {}, so using start_pos = 0".format(m6_start))
            prime_start_pos = 0
        else:
            logger.info("m6_start is {}, so using start_pos = 5".format(m6_start))
            prime_start_pos = 5

        linkedValues = HexValues(1, prime_start_pos, 1, 0) # magic starting "previous" values
        end_value = start_value + nvalues
        hfile = compute_hex_positions(start_value, end_value, linkedValues, save_opts)
        logger.info("save info: {}".format(save_opts))
        self.compute_next_chunks(hfile, nvalues, nchunks - 1, save_opts)

class HexValues(namedtuple('HexValues', 'prime pos spin rot')):
    """Holds data for prime hexagon computations, including prime, position, spin, rotation data.

    This class treats the values as opaque, and we store either single
    values and also the arrays for many values
    """
    
    @classmethod
    def from_text_file(cls, fname):
        prime, pos, spin, rot = np.loadtxt(fname, dtype=np.int64, delimiter=',', unpack=True)

        # ugh - single row of input gets returned as a set of scalar values. 
        if np.isscalar(prime):
            prime = np.array([prime])
            pos = np.array([pos])
            spin = np.array([spin])
            rot = np.array([rot])
        out = cls(prime, pos, spin, rot)
            
        return out

    @classmethod
    def from_binary_file(cls, fname):
        with np.load(fname, mmap_mode='r') as data:
            prime = data['prime']
            pos = data['pos']
            spin = data['spin']
            rot = data['rot']
        out = cls(prime, pos, spin, rot)
        return out
    

class HexDataFile:
    """HexDataFile is a helper to find ranges of our data on disk. Think of it as a mini-database that has some helper functions to retrieve the data we need.
"""
    def __init__(self, filename, require_exists=True):
        self._filename = filename
        if require_exists:
            _require_infile( filename )
        startval,endval,skip = self.get_params(filename)
        self._start = startval
        self._end   = endval
        self._skip  = skip
        self._last_values = None

    @property
    def filename(self): return self._filename
        
    @property
    def start(self): return self._start

    @property
    def end(self): return self._end

    @property
    def skip(self): return self._skip
    
    @staticmethod
    def get_params(filename):
        m = _HEX_FILENAME_RE.search(filename)
        if m is None or len(m.groups()) < 2:
            raise ValueError("filename {} does not have expected format".format(filename))
        groups = m.groupdict()
        if 'skip' not in groups or groups['skip'] is None:
            groups['skip'] = 1
        startval = long(groups['start'])
        endval   = long(groups['end'])
        skip     = long(groups['skip'])
        logger.info("found values from filename {} = {},{},{}".format(filename,startval,endval,skip))
        return (startval, endval, skip)

    @staticmethod
    def get_filename( start, end, save_opts):
        skip = save_opts.get('skip_interval',1)
        basename = save_opts.get('basename','output')
        fname = "{}-{:0>20d}-{:0>20d}-{:0>6d}".format(basename, start, end, skip)
        dprint(1,"new filename is {}".format(fname))
        return fname

    @classmethod
    def save_new_file( klass, start, end, data, save_opts):
        """Factory method for creating new HexDataFiles.

        Saves DATA to new files based on SAVE_OPTS. 

        Returns: a new HexDataFile instance for this new data
        """
        name = klass.get_filename(start, end, save_opts)

        # let's make sure output dir exists
        outdir = save_opts.get('dir','output')
        if not os.path.isdir(outdir):
            logger.info("creating output dir {}".format(outdir))
            os.makedirs(outdir)

        outname = None
        if save_opts.get('save_binary', False):
            outname = os.path.join(outdir, name) + '.npz'
            save_binary_arrays( outname, data, save_opts)

        if save_opts.get('save_text', False):
            outname = os.path.join(outdir, name) + '.txt'
            save_text_arrays( outname, data, save_opts=save_opts)

        if outname is None:
            logger.info("Must choose to save either binary or text files")
            raise Exception("Must choose either text or binary output files")

        newFile = klass(outname)
        newFile.set_last_values(data)
        newFile._end = end
        newFile._start = start
        newFile._skip = save_opts.get('skip_interval',1)
        return newFile
        
    def get_arrays(self):
        file,ext = os.path.splitext(self.filename)
        logger.info("file ext for {} is {}".format(self.filename,ext))
        if ext == '.npz':
            with np.load(self.filename, mmap_mode='r') as data:
                prime = data['prime']
                pos = data['pos']
                spin = data['spin']
                rot = data['rot']
        elif ext == '.txt':
            prime,pos,spin,rot = np.loadtxt(self.filename, delimiter=',', unpack=1, dtype=np.int64, ndmin=2)
        else:
            raise ValueError("unknown input file type with extension {}".format(ext))

        logger.info("loaded values from file={}".format(self.filename))
        logger.info("loaded values from prime={}".format(prime))
        logger.info("loaded values from pos={}".format(pos))
        logger.info("loaded values from spin={}".format(spin))
        logger.info("loaded values from rot={}".format(rot))
        return (prime, pos, spin, rot)

    def get_zipped_arrays_iterator(self):
        prime, pos, spin, rot = self.get_arrays()
        return zipper(prime, pos, spin,rot)

    def get_sliced_zipped_arrays_iterator(self, s):
        prime, pos, spin, rot = self.get_arrays()
        # not using itertools because it does not support -1 index'ed slicing
        return zipper(prime[s], pos[s], spin[s],rot[s])
    
    def contains_value(self, n):
        return self.start <= n and n <= self.end

    def contains_any_values(self, vals):
        for val in vals:
            if self.contains_value(val):
                return True
        return False
    
    def length(self):
        return self.end - self.start

    def set_last_values(self, data):
        self._last_values = HexValues(data.prime[-1], data.pos[-1], data.spin[-1], data.rot[-1])

    def get_last_values(self):
        if self._last_values is None:
            prime, pos, spin, rot = self.get_arrays()
            vals = HexValues(prime[-1], pos[-1], spin[-1], rot[-1])
            self._last_values = vals
        return self._last_values
    
    def __eq__(self, other):
        return self.start == other.start and self.end == other.end

    def __cmp__(self, other):
        if other is None:
            return 1
        start_cmp = cmp(self.start, other.start)
        if 0 != start_cmp:
            return start_cmp
        else:
            return cmp(self.end, other.end)
                    
    def __hash__(self):
        "HexDataFile hash."
        return hash(self.start) ^ hash(self.end)
                    
    def __str__(self):
        return "HexDataFile(file={},start={}, end={}, skip={})".format(self.filename, self.start, self.end,self.skip)
    
    def values_around(self, vals):
        cur_vals = []
        for x in vals:
            if self.contains_value(x):
                cur_vals.append(x)
        if not cur_vals:
            #sys.stderr.write("no values {} contained in HexDataFile {}\n".format(vals, self))
            return
        prime, pos, spin, rot = self.get_arrays()
        idx = prime.searchsorted(cur_vals)
        for ii in idx:
            yield ii
        
    def merge(self, other, outfile):
        # assert skip values are consistent...
        # can you only merge contiguous chunks?
        # you could just insertion sort the values...
        pass

    def print_sliced_values(self, slices, ofile = sys.stdout):
        for s in slices:
            logger.debug("getting slice {} {} {}".format(s.start, s.stop, s.step))
            data = self.get_sliced_zipped_arrays_iterator(s)
            for d in data:
                ofile.write( ','.join( map(str,d)) + '\n')
        
def get_slice_obj_from_str(slicearg):
    """Given a string that looks like a slice, return an actual slice object.
    This is used to let command line arguments specify slices.

    There is a wonky bit w/ argparse that conflicts with starting
    negative values. I keep forgetting to document the work around...

    """
    slicearg = re.sub(',','',slicearg)
    svals = [ int(n) if n else None for n in slicearg.split(':') ]
    svals = tuple(svals)
    s = slice(*svals)
    return s


def main(argv = None):
    import sys, argparse, os, re
    if argv is None:
        argv = sys.argv
            
    parser = argparse.ArgumentParser(description='Prime Spin Hexagons')
    parser.add_argument('--infile', help='Input file to start processing chunks')
    parser.add_argument('--startfrom', help="Starting point for provisional searching", type=long)
    parser.add_argument('--viewvalues', help='Values to view in the file as a python slice, e.g. 1:100:', action='append',)
    parser.add_argument('--find', help='Find values in files')
    parser.add_argument("-c", "--compress", help="flag to indicate whether or not to compress output files", action="store_true", default=True)
    parser.add_argument('--dir', help='Directory to read/write files to ',default='output')
    parser.add_argument('--basename', help='Basename of files to read and write', default='output')
    parser.add_argument('--logfile', help='Save messagse to this log file')
    parser.add_argument('--verbose', help='Print messages to the terminal', default=1)
    parser.add_argument('--save-text', help='Flag to save text files', action="store_true", default=False)
    parser.add_argument('--save-binary', help='Flag to save binary files',action="store_true", default=False)
    parser.add_argument('--use-cython', help='Flag to use cython implementation if available',dest="use_cython",action="store_true")
    parser.add_argument('--no-use-cython', help='Flag to not use cython implementation',dest="use_cython",action="store_false")
    parser.add_argument('--nvalues', help="number of values to process in a chunk",
                        default=10**9, type=long)
    parser.add_argument('--skip', help="0 means save only last value in each chunk. 1 means save all values",
                        default=0, type=long, choices=(0,1))
    parser.add_argument("--chunks", help="number of chunks to process", default=10,  type=int)
    args = parser.parse_args()
    
    global logger
    
    if args.logfile:
        fh = logging.FileHandler(args.logfile)
        fh.setLevel(logging.INFO)
        fh.setFormatter(log_formatter)
        # add the handlers to the logger
        logger.addHandler(fh)

    if args.verbose:
        # create console handler and set level to debug
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        # add formatter to ch
        ch.setFormatter(log_formatter)
        
        # add ch to logger
        logger.addHandler(ch)

    #setup_computation_engine(args.use_cython)

    if not os.path.isdir(args.dir):
        logger.info("creating output directory {}".format(args.dir))
        os.mkdir(args.dir)

    if args.skip != 0 and args.skip != 1:
        sys.stderr.write("Only valid skip values are 0 or 1\n")
        sys.exit(1)

    save_opts = { 'compress' : args.compress,
                  'skip_interval' : args.skip,
                  'save_text' : args.save_text,
                  'save_binary' : args.save_binary,
                  'dir' : args.dir,
                  'basename' : args.basename,
                  'engine' : 'cython' if args.use_cython else 'numpy'
    }
    
    run_opts = { 'nvalues' : args.nvalues,
                 'nchunks' : args.chunks }
    
    logger.info("Save options:" + str(save_opts))

    hexAssets = HexDataAssets(save_opts)
    if args.find:
        vals = [long(v) for v in args.find.split(',')]
        vals.sort()
        hexAssets.find_values_in_hexfiles(vals)
    elif args.viewvalues:
        _require_infile( args.infile )
        h = HexDataFile(args.infile)
        slices = [ get_slice_obj_from_str(s) for s in args.viewvalues]
        h.print_sliced_values(slices)
    else:
        if args.startfrom is not None:
            hexAssets.compute_provisional_chunks(args.startfrom, args.nvalues, args.chunks, save_opts)
        elif args.infile is not None:
            _require_infile( args.infile )
            start_file = HexDataFile(args.infile)
            hexAssets.compute_next_chunks(start_file, args.nvalues, args.chunks, save_opts)
        else:
            hexAssets.compute_initial_chunks(args.nvalues, args.chunks, save_opts)
        

if __name__ == "__main__":
    import sys
    main(sys.argv)



