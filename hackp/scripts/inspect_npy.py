import argparse
import numpy as np

if __name__=='__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", type=str, required=True, help='The path to an input npy file')
    args = parser.parse_args()

    data = np.load(args.file)
    print(data)
    print(data.shape)
