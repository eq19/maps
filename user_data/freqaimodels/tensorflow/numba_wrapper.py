import numba

# export NUMBA_NUM_THREADS='4'
# export NUMBA_ENABLE_CUDASIM='1'
# export NUMBA_DEBUG_PRINT_AFTER='ir_legalization'

def _jit(*args, **kwargs):
    if 'nopython' not in kwargs:
        kwargs['nopython'] = True

    if 'cache' not in kwargs:
        kwargs['cache'] = True

    if 'inline' not in kwargs and False:
        kwargs['inline'] = 'always'

    return numba.core.decorators.jit(*args, **kwargs)

numba.jit = _jit
numba.Dict = numba.typed.Dict
numba.List = numba.typed.List
