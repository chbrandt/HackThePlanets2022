import argparse
import matplotlib
import numpy as np
from os import listdir
from pathlib import Path
import matplotlib.pyplot as plt

def export_img(input_npy, size, how_many):

    regions = np.load(input_npy)

    print(f"Regions shape: {regions.shape}")

    for i, region in enumerate(regions[0:how_many]):
        plt.figure()
        ax = plt.subplot()
        ax.imshow(region.reshape(size,size), cmap="magma")
        plt.savefig(f"{input_npy.stem}-{args.size}-{i}.png", dpi=250)
        plt.close()

if __name__=='__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", type=str, required=True, help='The path to an input file in .npy format or a directory')
    parser.add_argument("-sz", "--size", type=int, required=True, help='The size of the input square images')
    parser.add_argument("-hm", "--how-many", type=int, required=True, help='How many .png files will be produced for each .npy')
    args = parser.parse_args()

    input_fd = Path(args.input)

    if input_fd.is_file():

            export_img(input_fd, args.size, args.how_many)

    elif input_fd.is_dir():

        npy_files = [input_fd.joinpath(f) for f in listdir(input_fd)]

        # TODO: parallelize me!
        
        for input_npy in npy_files:
            export_img(input_npy, args.size, args.how_many)
