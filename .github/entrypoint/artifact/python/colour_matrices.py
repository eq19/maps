#!/usr/bin/env python3
"""Small program to explore colour matrices and structure constants in QCD.

Written by Gavin Salam as an illustration for lecture 1 of the QCD
course at the 2024 European School of High-Energy Physics.
"""
import numpy as np

def main():

    print("Warning: the A,B,C indices here run from 0 to 7, not 1 to 8 as in the lecture notes.")
    print("Warning: the a,b,c indices here run from 0 to 2, not 1 to 3 as in the lecture notes.")

    nF = 3 # number of degrees of freedom in Fundamental representation (quarks)
    nA = 8 # number of degrees of freedom in Adjoint representation (gluos)
    lambdas = get_lambdas()
    ts = [0.5*l for l in lambdas]

    #---------------------------------------------
    header("check Tr(t^A t^B) = T_R delta^{AB}")
    for A in range(nA):
        for B in range(nA):
            trace = np.trace(np.matmul(ts[A],ts[B]))
            if abs(trace)>1e-10: print(f"{A=} {B=}: Trace(t^A t^B)={trace}")

    #---------------------------------------------
    header("check Sum_A(t_{ab}^A t_{bc}^A) = C_F \\delta_{ac}")
    sum = np.zeros((3,3),dtype=complex)
    for A in range(nA):
        sum += np.matmul(ts[A],ts[A])
    for a in range(nF):
        for c in range(nF):
            print(f"{a=} {c=}: Sum_A(t_{{ab}}^A t_{{bc}}^A)={sum[a][c]}")

    #---------------------------------------------
    header("Examine the non-zero fABCs (A<B<C)")
    fABCs = get_fABCs(ts)
    for A in range(nA):
        for B in range(A+1,nA):
            entries = non_zero_entries(fABCs[A,B,:],B+1,'C')
            if entries: print(f"{A=} {B=}, {entries}")

    #---------------------------------------------
    header("check Sum_{C,D} f^{ACD} f^{BCD} = C_A delta^{AB}")
    for A in range(nA):
        for B in range(nA):
            result = np.sum(fABCs[A,:,:] * fABCs[B,:,:])
            if abs(result) > 1e-10: print(f"{A=} {B=} {result=}")

def header(title):
    print()
    print("-"*len(title))
    print(title)
    print("-"*len(title))

def non_zero_entries(arr,imin, tag="i"):
    res = []
    for i in range(imin, arr.shape[0]):
        if abs(arr[i]) > 1e-10: res.append(f"{tag}={i}:{arr[i]}")
    return ", ".join(res)

def get_fABCs(ts):
    "returns the fABC array"

    # get the ts supplemented by a unit array, which is needed to
    # complete the basis below that we will use in solving for the fABCs
    ts_plus_unit = np.array([t.flatten() 
                            for t in ts+[np.diag(np.array([1,1,1],dtype=complex))] ])

    nA = len(ts)
    fABC = np.zeros((nA,nA,nA))
    for A in range(nA):
        for B in range(nA):
            tt = (np.matmul(ts[A],ts[B]) - np.matmul(ts[B],ts[A]))/complex(0,1)
            ff = np.linalg.solve(ts_plus_unit.transpose(), tt.flatten())
            if abs(ff[nA]) > 1e-10: raise("illegal 9th component in nA")
            fABC[A,B,:] = np.real(ff[:nA])
            #if B <= A: continue
            #print(f"{A=} {B=}, fABC={fABC[A,B,:]}")

    return fABC


def get_lambdas():
    """Return the Gell-Mann matrices as a list of 3x3 numpy arrays."""
    i = complex(0,1)
    lambdas = [0]*8
    lambdas[0] = [[ 0, 1, 0],
                  [ 1, 0, 0],
                  [ 0, 0, 0]]

    lambdas[1] = [[ 0,-i, 0],
                  [ i, 0, 0],
                  [ 0, 0, 0]]

    lambdas[2] = [[ 1, 0, 0],
                  [ 0,-1, 0],
                  [ 0, 0, 0]]

    lambdas[3] = [[ 0, 0, 1],
                  [ 0, 0, 0],
                  [ 1, 0, 0]]
    
    lambdas[4] = [[ 0, 0,-i],
                  [ 0, 0, 0],
                  [ i, 0, 0]]
    
    lambdas[5] = [[ 0, 0, 0],
                  [ 0, 0, 1],
                  [ 0, 1, 0]]
    
    lambdas[6] = [[ 0, 0, 0],
                  [ 0, 0,-i],
                  [ 0, i, 0]]
    
    lambdas[7] = [[ 1.0/np.sqrt(3), 0, 0],
                  [ 0, 1.0/np.sqrt(3), 0],
                  [ 0, 0,-2.0/np.sqrt(3)]]
    
    return [np.array(l,dtype=complex) for l in lambdas]

if __name__ == "__main__":
    main()
