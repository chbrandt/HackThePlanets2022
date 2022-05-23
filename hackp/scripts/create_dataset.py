import os
import argparse
import numpy as np
from os import listdir
import multiprocessing
from pathlib import Path
from functools import partial 

from hackp.utils.tif import read_tif
from hackp.utils.imgproc import extract_regions

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'


def extract_patch_and_save(output_dir, tif_file):

    output_file = output_dir.joinpath(tif_file.stem).with_suffix(".npy")

    if not output_file.exists():

        print(f"Opening: {tif_file.stem}")

        regions = extract_regions(read_tif(tif_file), args.size, args.stride)

        print(f"Extracted images: {len(regions)} with shape {regions[0].shape}")

        if args.format == "npy":
            np.save(output_file, regions)

        elif args.format == "png":
            pass



if __name__=='__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--dataset", type=str, required=True, help='The path to an input direcotry containing .tif files')
    parser.add_argument("-o", "--output", type=str, required=True, help='The path to an output direcotry that will contain the output files')
    parser.add_argument("-sz", "--size", type=int, required=True, help='The size of the square images that are going to be extracted')
    parser.add_argument("-st", "--stride", type=int, required=True, help='If stride==size, there will be no overlapping')
    parser.add_argument("-f", "--format", type=str, required=True, choices=["npy", "png"], help="The output file format")
    parser.add_argument("-nj", "--njobs", type=int, required=True, help="The number of worker threads")
    args = parser.parse_args()

    dataset = Path(args.dataset)

    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    unzipped_data_files = [dataset.joinpath(f) for f in listdir(dataset) if dataset.joinpath(f).exists()]

    pool = multiprocessing.Pool(processes=args.njobs)

    pool.map(partial(extract_patch_and_save, output_dir), unzipped_data_files)
