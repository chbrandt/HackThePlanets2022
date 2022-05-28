import argparse
import matplotlib
import numpy as np
from os import listdir
import multiprocessing
from pathlib import Path
from functools import partial
import matplotlib.pyplot as plt

def export_img(size, how_many, output_dir, input_npy):

    regions = np.load(input_npy)

    print(f"Regions shape: {regions.shape}")

    for i, region in enumerate(regions[0:how_many]):
        plt.figure()
        ax = plt.subplot()
        ax.imshow(region.reshape(size,size), cmap="magma")
        out_filename = output_dir.joinpath(f"{input_npy.stem}-{args.size}-{i}.png")
        plt.savefig(out_filename, dpi=250)
        plt.close()
    
    return regions.shape[0]

if __name__=='__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", type=str, required=True, help='The path to an input file in .npy format or a directory')
    parser.add_argument("-sz", "--size", type=int, required=True, help='The size of the input square images')
    parser.add_argument("-hm", "--how-many", type=int, required=True, help='How many .png files will be produced for each .npy')
    parser.add_argument("-od", "--output-dir", type=str, required=True, help='The path to the output directory')
    parser.add_argument("-nj", "--njobs", type=int, required=True, help="The number of worker threads")
    args = parser.parse_args()

    input_fd = Path(args.input)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    number_of_maps = 0

    if input_fd.is_file():

        npy_files = [input_fd]

    elif input_fd.is_dir():

        npy_files = [input_fd.joinpath(f) for f in listdir(input_fd)]

    print(f"Number of files to process: {len(npy_files)}")
    
    with multiprocessing.Pool(processes=args.njobs) as pool:

        number_of_maps = pool.map(partial(export_img, args.size, args.how_many, output_dir), npy_files)

        print(f"Total number of maps: {sum(number_of_maps)}")

