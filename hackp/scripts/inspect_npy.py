import argparse
import numpy as np
from time import time

if __name__=='__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", type=str, required=True, help='The path to an input npy file')
    args = parser.parse_args()

    s = time()
    data = np.load(args.file)
    print(f"Loading took {time()-s} s")
    print(data)
    print(data.shape)
