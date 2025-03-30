
import os
import pytest
import primespin
import numpy

primes_100 = [2, 3, 5, 7, 11, 13, 17, 19, 23,
              29, 31, 37, 41, 43, 47, 53, 59,
              61, 67, 71, 73, 79, 83, 89, 97]


@pytest.mark.parametrize("last", [10,100,1000,10**5])
@pytest.mark.parametrize("first", [1, 10,100,1000])
def test_primes_implementations_are_equal(first, last):
    a1 = primespin.numpy_generate_primes_array(first, last)
    a2 = primespin.list_generate_primes_array(first, last)
    numpy.testing.assert_equal( a1, a2)

def test_primes_implementations_are_correct():
    a1 = primespin.numpy_generate_primes_array(1,100)
    a2 = primespin.list_generate_primes_array(1,100)
    b = numpy.array(primes_100)
    numpy.testing.assert_equal( a1, b)
    numpy.testing.assert_equal( a2, b)

def split_hex_values_into_chunks_and_slice( hval, nvalues, nchunks, skip_interval):

    if skip_interval == 0:
        skip_slice = slice(-1,None, None)
    else:
        skip_slice = slice(None,None, skip_interval)
    nn = hval.prime.shape[0]
    sz = int(nn/nchunks)
    print("nvalues={} nchunks={} nn = {} and sz={} slice={}".format(nvalues, nchunks, nn, sz, skip_slice))

    prime, pos, rot, spin = [numpy.empty(0,dtype=numpy.int64) for x in range(4)]
    prev = 0
    for ii in range(0, nchunks*nvalues, nvalues):
        cur = numpy.searchsorted(hval.prime, ii + nvalues)
        s = slice(prev, cur)
        primenew = hval.prime[s][skip_slice]
        posnew   = hval.pos[s][skip_slice]
        spinnew  = hval.spin[s][skip_slice]
        rotnew   = hval.rot[s][skip_slice]
        print("new prime = {}".format(primenew))
        print("new pos = {}".format(posnew))
        prime = numpy.append(prime, primenew)
        pos   = numpy.append(pos, posnew)
        spin  = numpy.append(spin, spinnew)
        rot   = numpy.append(rot,  rotnew)
        prev = cur

    print("finished prime={}".format(prime))
    return primespin.HexValues(prime, pos, spin, rot)
        
def load_arrays_from_partial_hex_files( files ):
    prime,pos,rot,spin = [numpy.empty(0,dtype=numpy.int64) for x in range(4)]
    for f in files:
        a = load_hex_values_from_file(f)
        prime = numpy.append(prime, a.prime)
        print("load prime = {}".format(a.prime))
        print("load pos = {}".format(a.pos))
        pos   = numpy.append(pos, a.pos)
        spin  = numpy.append(spin, a.spin)
        rot   = numpy.append(rot, a.rot)
    out = primespin.HexValues( prime, pos, spin, rot)
    return out

def slice_hex_values( hvals, sliceobj ):
    return primespin.HexValues( hvals.prime[sliceobj],
                                hvals.pos[sliceobj],
                                hvals.spin[sliceobj],
                                hvals.rot[sliceobj])

def load_hex_values_from_file( fn):
    fn = str(fn)
    if fn.endswith('.txt'):
        vals = primespin.HexValues.from_text_file(fn)
    elif fn.endswith('.npz'):
        vals = primespin.HexValues.from_binary_file(fn)
    else:
        raise IOError("unknown array file type {}".format(fn))
    return vals

def assert_hex_arrays_are_equal( h1, h2):
    numpy.testing.assert_equal( h1.prime, h2.prime)
    numpy.testing.assert_equal( h1.pos, h2.pos)
    numpy.testing.assert_equal( h1.spin, h2.spin)
    numpy.testing.assert_equal( h1.rot, h2.rot)

def assert_hex_array_files_are_equal( fn1, fn2 ):
    arrs1 = load_hex_values_from_file(fn1)
    arrs2 = load_hex_values_from_file(fn2)
    assert_hex_arrays_are_equal( arrs1, arrs2 )
        
def assert_npy_files_are_equal(fn1, fn2):
    arrs1 = primespin.HexValues.from_binary_file(fn1)
    arrs2 = primespin.HexValues.from_binary_file(fn2)
    assert_hex_arrays_are_equal( arrs1, arrs2 )
    
def assert_text_file_arrays_are_equal(fn1, fn2):
    arrs1 = primespin.HexValues.from_text_file( fn1 )
    arrs2 = primespin.HexValues.from_text_file( fn2 ) 
    assert_hex_arrays_are_equal( arrs1, arrs2 )

        
def is_numpy_file(f):
    _, ext = os.path.splitext( str(f) )
    return ext in ('.npy','.npz')

def is_txt_file(f):
    _, ext = os.path.splitext( str(f) )
    return ext in ('.txt')

@pytest.mark.parametrize("nchunks", [1, 2, 5, 20])
@pytest.mark.parametrize("nvalues", [100,10**5])
def test_compare_numpy_and_cython_implementations(tmpdir, nvalues, nchunks):

    testname = get_test_name()
    base_opts =  { 'compress' : True,
                   'skip_interval' : 1,
                   'save_text' : True,
                   'dir' : None,
                   'basename' : 'output',
                   'engine' : 'cython',
                   'nvalues' : nvalues,
                   'nchunks' : nchunks
    }

    d1 = tmpdir.mkdir(testname + "_cython")
    opt1 = base_opts.copy()
    opt1['engine'] = 'cython'
    opt1['dir'] = str(d1)
    h1 = primespin.HexDataAssets(opt1)
    h1.compute_initial_chunks(opt1['nvalues'], opt1['nchunks'], opt1)

    d2 = tmpdir.mkdir(testname + "_numpy")
    opt2 = base_opts.copy()
    opt2['engine'] = 'numpy'
    opt2['dir'] = str(d2)
    h2 = primespin.HexDataAssets(opt2)
    h2.compute_initial_chunks(opt2['nvalues'], opt2['nchunks'], opt2)

    # output dirs were made
    assert os.path.isdir(str(d1))
    assert os.path.isdir(str(d2))

    import filecmp
    dircmp = filecmp.dircmp( str(d1), str(d2) )

    # Confirm all txt files match
    #   we should have nchunks matching text files
    same_txt_files = [item for item in dircmp.same_files if is_txt_file(item)]
    assert len(same_txt_files) == nchunks

    #   we should have no mismatching text files
    diff_txt_files = [item for item in dircmp.diff_files if is_txt_file(item)]
    assert len(diff_txt_files) == 0

    # Assume npy files are byte-wise different but same underlying values
    #   but they might just match, so handle that too

    # get same and diff file lists
    diff_npy_files = [item for item in dircmp.diff_files if is_numpy_file(item)]
    same_npy_files = [item for item in dircmp.same_files if is_numpy_file(item)]

    # should have NCHUNKS npy files total, either same or diff
    assert len(diff_npy_files) + len(same_npy_files) == nchunks
    
    # check all diff npy/npz files are numpy equal
    for f in diff_npy_files:
        f1,f2 = d1.join(f), d2.join(f)
        assert_npy_files_are_equal( str(f1), str(f2) )

@pytest.mark.parametrize("nchunks", [1, 2, 5, 20])
@pytest.mark.parametrize("nvalues", [100, 1000, 10**5])
@pytest.mark.parametrize("engine", ['cython','numpy'])
def test_binary_and_text_outputs_are_equal(tmpdir, nchunks, nvalues, engine):
    testname = get_test_name()

    d1 = tmpdir.mkdir(testname)
    base_opts =  { 'compress' : True,
                   'skip_interval' : 1,
                   'save_text' : True,
                   'dir' : str(d1),
                   'basename' : 'output',
                   'engine' : engine,
                   'nvalues' : nvalues,
                   'nchunks' : nchunks
    }

    opt1 = base_opts.copy()
    do_one_run(opt1, d1)

    assert os.path.isdir(str(d1))

    files = d1.listdir()
    txt_files = sorted(filter(is_txt_file, files))
    npy_files = sorted(filter(is_numpy_file, files))

    # we should have the same number of output files
    assert len(txt_files) == len(npy_files)

    # check that corresponding files are numerically equal
    iter = zip(txt_files, npy_files )
    for files in iter:
        txt, npy = files
        assert_hex_array_files_are_equal( txt, npy )

    # now test that they equal the known good values
    
# test compression 
#    run with and without compression
#    assert values are the same but compressed version is smaller in size

# test skip values
#    write out 1000 with skip 10
#    confirm with 1000-valid values, skipping every 10

# DONE: test that chunking works:
#    chunk 100x10 values
#    compare that all 100x10 values == the 1000 known values

# test resuming works:
#   generate initial chunk 0-100 as file
#   resume generate chunk 100-200 starting from previous chunk
#   compare the values 0-100 + 100-200 are correct compared to ground truth

def get_test_name():
    """ return the name of the calling function after removing leading test_ prefix"""
    import inspect
    testname = inspect.stack()[1][3]
    if testname.startswith("test_"):
        testname = testname[5:]
    return testname

_base_opts =  { 'compress' : True,
               'skip_interval' : 1,
               'save_text' : True,
               'dir' : 'output',
               'basename' : 'output',
               'engine' : 'cython',
               'nchunks': 1,
               'nvalues': 1000
}

def do_one_run(opts, dirname):
    h1 = primespin.HexDataAssets(opts)
    h1.compute_initial_chunks(opts['nvalues'], opts['nchunks'], opts)


@pytest.mark.parametrize("nchunks", [1,4,10,50])
@pytest.mark.parametrize("engine", ['numpy','cython'])
@pytest.mark.parametrize("skip_interval", [0,1])
def test_vs_known_good_values(tmpdir, nchunks, engine,skip_interval):

    testname = get_test_name()
    nvalues = int(1000/nchunks)
    d1 = tmpdir.mkdir(testname)
    base_opts = { 'compress' : True,
                  'skip_interval' : skip_interval,
                  'save_text' : True,
                  'dir' : str(d1),
                  'basename' : 'output',
                  'engine' : engine,
                  'nchunks' : nchunks,
                  'nvalues' : nvalues
    }

    opt1 =  base_opts.copy()
    do_one_run(opt1, d1)

    # check output dirs were made
    assert os.path.isdir(str(d1))

    files = d1.listdir()
    txt_files = sorted(filter(is_txt_file, files))
    npy_files = sorted(filter(is_numpy_file, files))

    # compare 1000 known values with output arrays
    good_file = os.path.join(os.path.dirname(__file__), 'good-0000-1000-01.txt')
    good_arrs = load_hex_values_from_file(good_file)
    
    sliced_good_arrs = split_hex_values_into_chunks_and_slice(good_arrs, nvalues, nchunks, skip_interval)
    print("sliced good prime is\n{} ".format(sliced_good_arrs.prime))
    print("sliced good pos is\n{}".format(sliced_good_arrs.pos))
    print("sliced good spin is\n{}".format(sliced_good_arrs.spin))
    print("sliced good rot is\n{}".format(sliced_good_arrs.rot))
    
    txt_arrs = load_arrays_from_partial_hex_files( txt_files )
    npy_arrs = load_arrays_from_partial_hex_files( npy_files )

    print("txt prime is\n{} ".format(txt_arrs.prime))
    print("txt pos is\n{}".format(txt_arrs.pos))
    print("txt spin is\n{}".format(txt_arrs.spin))
    print("txt rot is\n{}".format(txt_arrs.rot))

    print("npy prime is\n{} ".format(txt_arrs.prime))
    print("npy pos is\n{}".format(txt_arrs.pos))
    print("npy spin is\n{}".format(txt_arrs.spin))
    print("npy rot is\n{}".format(txt_arrs.rot))

    assert_hex_arrays_are_equal(npy_arrs, txt_arrs)
    
    assert_hex_arrays_are_equal(sliced_good_arrs, txt_arrs)

    assert_hex_arrays_are_equal(sliced_good_arrs, npy_arrs)

    
