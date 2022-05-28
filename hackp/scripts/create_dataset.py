import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '0'
import argparse
import numpy as np
from os import listdir
import multiprocessing
from pathlib import Path
from functools import partial 

from hackp.utils.tif import read_tif
from hackp.utils.imgproc import extract_regions


def save_img(img, output_dir, format, filename):

    output_file = output_dir.joinpath(filename).with_suffix(".npy")

    if not output_file.exists():

        if format == "npy":
            # print(f"Saving {output_file}")
            np.save(output_file, img)

        elif format == "png":
            pass

    
def extract_patch_and_save(output_dir, format, tif_file):

        print(f"Opening: {tif_file.stem}")

        regions = np.expand_dims( 
                        extract_regions(read_tif(tif_file), args.size, args.stride)
                            .reshape(-1, args.size, args.size)
        , axis=-1) # => (N,H,W,C)

        print(f"Extracted images: {regions.shape}") # (N, H, W)

        for idx,region in enumerate(regions):
            save_img(region, output_dir, format, tif_file.stem+f"_{idx}")

        return regions.shape[0]



if __name__=='__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--dataset", type=str, required=True, help='The path to an input direcotry containing .tif files')
    parser.add_argument("-o", "--output", type=str, required=True, help='The path to an output direcotry that will contain the output files')
    parser.add_argument("-sz", "--size", type=int, required=True, help='The size of the square images that are going to be extracted')
    parser.add_argument("-st", "--stride", type=int, required=True, help='If stride==size, there will be no overlapping')
    parser.add_argument("-f", "--format", type=str, required=True, choices=["npy", "png"], help="The output file format")
    parser.add_argument("-nrj", "--n-reader-jobs", type=int, required=False, default=2, help="The number of worker reader threads")
    args = parser.parse_args()

    dataset = Path(args.dataset)

    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    unzipped_data_files = [dataset.joinpath(f) for f in listdir(dataset) if dataset.joinpath(f).exists()]

    with multiprocessing.Pool(processes=args.n_reader_jobs) as pool:

        maps = pool.map(partial(extract_patch_and_save, output_dir, args.format), unzipped_data_files)

        print(f"Total files produced: {sum(maps)}")