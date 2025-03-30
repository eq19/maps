#!/usr/bin/python
"""
Map Prime Hexagon calculation

by Julian Gutierrez
NUCAR High Performance Computing
2017

"""
import argparse
import numpy as np

if __name__ == "__main__":
   
    parser = argparse.ArgumentParser(description = 'Prime Hexagon: NPZ Reader',formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--file',        default = "./",          type=str,               help='File to read data from.')
    args = parser.parse_args()

    with np.load(args.file, mmap_mode='r', allow_pickle=True) as data:
            prime = data['prime'][0]
            pos = data['pos'][0]
            spin = data['spin'][0]
            rot = data['rot'][0]
            print(prime, pos, spin, rot)
