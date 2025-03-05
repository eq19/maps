"""Generate generalized Gell-Mann matrices.

  .. module:: gellmann.py
     :synopsis: Generate generalized Gell-Mann matrices
  .. moduleauthor:: Jonathan Gross <jarthurgross@gmail.com>

  .. references::
     - https://arxiv.org/pdf/0806.1174.pdf
     - https://github.com/iree-org/iree/tree/main/integrations/pjrt
     - https://mathworld.wolfram.com/GeneralizedGell-MannMatrix.html
     - https://github.com/husisy/klearning/blob/master/misc/draft_gellman.py

"""
import numpy as np
import itertools as it

from pylab import *
from sparse import COO
from pprint import pprint

def gellmann(j, k, d, sparse=False):
    r"""Returns a generalized Gell-Mann matrix of dimension d.

    According to the convention in *Bloch Vectors for Qubits* by Bertlmann and
    Krammer (2008), returns :math:`\Lambda^j` for :math:`1\leq j=k\leq d-1`,
    :math:`\Lambda^{kj}_s` for :math:`1\leq k<j\leq d`, :math:`\Lambda^{jk}_a`
    for :math:`1\leq j<k\leq d`, and :math:`I` for :math:`j=k=d`.

    Parameters
    ----------
    j : positive integer
        Index for generalized Gell-Mann matrix
    k : positive integer
        Index for generalized Gell-Mann matrix
    d : positive integer
        Dimension of the generalized Gell-Mann matrix

    Returns
    -------
    numpy.array
        A genereralized Gell-Mann matrix.

    """

    if j > k:
        coords = [[j - 1, k - 1],
                  [k - 1, j - 1]]
        data = [1, 1]
    elif k > j:
        coords = [[j - 1, k - 1],
                  [k - 1, j - 1]]
        data = [-1j, 1j]
    elif j == k and j < d:
        coords = [list(range(j + 1)),
                  list(range(j + 1))]
        data = np.sqrt(2/(j*(j + 1)))*np.array(list(it.repeat(1 + 0j, j))
                                               + [-j + 0j])
    else:
        coords = [list(range(d)),
                  list(range(d))]
        data = list(it.repeat(1 + 0j, d))

    if sparse:
        gjkd = COO(coords, data, shape=(d, d))
    else:
        gjkd = np.zeros((d, d), dtype=np.complex128)
        for val, m, n in zip(data, *coords):
            gjkd[m][n] = val

    return gjkd

def get_basis(d, sparse=False):
    r"""Return a basis of operators.

    The basis is made up of orthogonal Hermitian operators on a Hilbert space
    of dimension d, with the identity element in the last place.

    Parameters
    ----------
    d : int
        The dimension of the Hilbert space.

    Returns
    -------
    list of numpy.array
        The basis of operators.

    """
    return [gellmann(j, k, d, sparse)
            for j, k in it.product(range(1, d + 1), repeat=2)]

pprint(get_basis(13))
