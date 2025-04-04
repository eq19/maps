
from libc.stdint cimport uint64_t, int64_t, int32_t, int8_t

cimport numpy as np
import numpy as np

import logging

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


cpdef np.ndarray _compute_spins(np.ndarray[np.uint64_t, ndim=1,mode='c'] primes, uint64_t last_prime, int last_spin, out = None):
    """Returns array of SPINS given an array of PRIMES (assumed to be 1d)

    SPINS result array is same shape as PRIMES, with values stored in SPINS[1:]; 
    SPINS[0] = 0, use that zero element to thread chunked computations together.
    """
    
    global logger

    cdef uint64_t nn = primes.shape[0]

    cdef np.ndarray[np.int8_t, ndim=1, mode='c'] out_array
    if out is None or nn > out.shape[0]:
        out_array = np.empty([nn], dtype=np.int8, order='c')
    else:
        out_array = out
        
    logger.info("compute_spins: starting computing spins")

    cdef uint64_t *pdata
    cdef int8_t   *odata

    cdef int m6val_prev = last_prime % 6
    cdef int m6val_cur
    cdef int m6_offset_sum
    cdef int z

    cdef int8_t cumprod_val  = last_spin
    cdef uint64_t ii
    for ii in range(0, nn):
        pdata = <uint64_t *>(np.PyArray_GETPTR1(primes, ii))
        m6val_cur = pdata[0] % 6

        #logger.info("compute_spins: for ii = {} m6val prev {} and cur {}".format(ii, m6val_prev,m6val_cur))
        m6_offset_sum = m6val_prev + m6val_cur
        if m6_offset_sum == 6:
            z = 1
        elif ((m6_offset_sum == 10) or (m6_offset_sum == 2)):
            z = -1
        else:
            #z = 0
            raise ValueError("m6_offset_sum != 6,10 or 2 at position {}: {}".format(ii, m6_offset_sum))
        
        cumprod_val *= z
        # out_array[ii] = cumprod_val
        odata = <int8_t *>(np.PyArray_GETPTR1(out_array, ii))
        odata[0] = cumprod_val

        # shift next values into current values
        m6val_prev = m6val_cur

    #logger.info("compute_spins: generating mod6Values")
    #m6val  = primes % 6
    #m6_offset_sum     = np.empty_like(primes, dtype=np.int32)
    #m6_offset_sum[0]  = m6val[0] + (last_prime % 6)            #  seed value from current val + prev m6val
    #m6_offset_sum[1:] = m6val[1:] + m6val[:-1]                 #  cur m6val + prev m6val
    #logger.info("compute_spins: done mod6Values")

    #logger.info("compute_spins: starting to compute spins")

    #z = np.zeros_like(primes, dtype=np.int32)
    #z[ m6_offset_sum ==  6] =  1
    #z[ m6_offset_sum == 10] = -1
    #z[ m6_offset_sum ==  2] = -1
    #spin = np.cumprod(z)

    logger.info("compute_spins: done computing spins")
    return out_array



cpdef np.ndarray  _compute_positions(np.ndarray[np.int8_t, ndim=1, mode='c'] spin, int seed_pos, int seed_spin, out = None):
    """Given an array of SPINS and two SEED_POSITION and SEED_SPIN values, compute the positions along the prime hex 

    """

    global logger
    logger.info("compute_positions: starting primary calculation")

    cdef uint64_t nn = spin.shape[0]

    cdef np.ndarray[np.int8_t, ndim=1, mode='c'] out_array
    if out is None or nn > out.shape[0]:
        out_array = np.empty([nn], dtype=np.int8, order='c')
    else:
        out_array = out

    cdef int8_t *sdata_cur
    cdef int8_t *odata

    cdef int8_t spin_prev = seed_spin
    cdef int8_t spin_cur
    cdef int8_t delta
    cdef int64_t cumsum_val = seed_pos
    cdef int8_t increment
    cdef uint64_t ii
    for ii in range(0,nn):
        
        #spin_cur = spin[ii]
        sdata_cur  = <int8_t *>(np.PyArray_GETPTR1(spin, ii))
        spin_cur = sdata_cur[0]
        delta = spin_cur - spin_prev
        if delta == 0:
            increment = abs(spin_cur)
        else:
            increment = 0
        cumsum_val += increment

        #out_array[ii] = cumsum_val % 6
        odata = <int8_t *>(np.PyArray_GETPTR1(out_array, ii))
        odata[0] = cumsum_val % 6

        # save cur spin for next round as prev value
        spin_prev = spin_cur
        
    #delta = np.zeros_like(spin,dtype=np.int32)
    #delta[0]  = spin[0] - seed_spin      # first delta is seed_spin from previous chunk to this first spin
    #delta[1:] = spin[1:] - spin[0:-1]    # compute rest of deltas from input spins array

    #increments = np.copy(spin)           # copy the spin array,
    #increments[ delta != 0 ] = 0         # set any non-zero delta to zero in the increment array

    #logger.info("compute_positions:\tdone with aux calculations")
    
    #logger.info("compute_positions: starting primary calculation")

    # start at seed, cumulative add
    #positions = np.copy(increments)
    #positions[0] += seed_pos
    #outpositions = np.cumsum(positions) % 6
    logger.info("compute_positions:\tdone with primary calculation")
    #return outpositions
    return out_array


cpdef np.ndarray _compute_rotations(np.ndarray[np.int8_t, ndim=1, mode='c'] positions, int pos_seed, int64_t rot_seed, out = None):

    global logger
    logger.info("compute_rotations: starting primary calculations")
    #logger.info("compute_rotations: starting aux calculations")

    cdef uint64_t nn = positions.shape[0]

    cdef np.ndarray[np.int64_t, ndim=1, mode='c'] out_array
    if out is None or nn > out.shape[0]:
        out_array = np.empty([nn], dtype=np.int64, order='c')
    else:
        out_array = out

    cdef int8_t *pdata
    cdef int64_t *odata

    cdef int8_t pos_cur
    cdef int8_t pos_prev = pos_seed
    cdef int8_t delta
    cdef int64_t cumsum_val = rot_seed
    cdef int8_t inc
    cdef uint64_t ii

    for ii in range(0, nn):
        
        #pos_cur= positions[ii]
        pdata  = <int8_t *>(np.PyArray_GETPTR1(positions, ii))
        pos_cur = pdata[0]
        delta = pos_cur - pos_prev
        if delta == -5:
            inc = 1
        elif delta == 5:
            inc = -1
        else:
            inc = 0
        cumsum_val += inc

        #out_array[ii] = cumsum_val
        odata = <int64_t *>(np.PyArray_GETPTR1(out_array, ii))
        odata[0] = cumsum_val

        # save cur spin for next round as prev value
        pos_prev = pos_cur
        

    #delta = np.zeros_like(positions)
    #delta[1:] = positions[1:] - positions[:-1]
    #delta[0] = positions[0] - pos_seed

    #z = np.zeros_like(delta)       # zero array like delta
    #z[ delta == -5 ] =  1          # where delta = -5, set increment to 1
    #z[ delta ==  5 ] = -1          # where delta is 5, set increment to -1
    #logger.info("compute_rotations: done with aux calculations")

    #logger.info("compute_rotations: starting primary calculations")
    # z[0] += rot_seed
    # r = np.cumsum( z )
    logger.info("compute_rotations: done with primary calculations")

    #return r
    
    return out_array


    
        


