import argparse
import matplotlib
import numpy as np
matplotlib.use('agg')
import matplotlib.pyplot as plt


if __name__=='__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("-if", "--input-file", type=str, required=True, help='The path to an input file in .npy format')
    parser.add_argument("-sz", "--size", type=int, required=True, help='The size of the input square image')
    parser.add_argument("-hm", "--how-many", type=int, required=True, help='How many .png files will be produced')
    args = parser.parse_args()

    regions = np.load(args.input_file)

    print(f"Regions shape: {regions.shape}")

    for i, region in enumerate(regions[0:args.how_many]):
        plt.figure()
        ax = plt.subplot()
        ax.imshow(region.reshape(args.size,args.size), cmap="magma")
        plt.savefig(f"{args.size}-{i}.png", dpi=500)
    