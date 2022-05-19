import argparse
import numpy as np
from tqdm import tqdm
from os import listdir
from pathlib import Path

from hackp.utils.imgproc import read_tiff, extract_regions

if __name__=='__main__':

    # TODO: datapath, outputpath, size and stride as input args
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--dataset", type=str, required=True, help='The path to an input direcotry containing .tif files')
    parser.add_argument("-o", "--output", type=str, required=True, help='The path to an output direcotry that will contain .npy files')
    parser.add_argument("-sz", "--size", type=int, required=True, help='The size of the square images that are going to be extracted')
    parser.add_argument("-st", "--stride", type=int, required=True, help='If stride==size, there will be no overlapping')
    args = parser.parse_args()

    dataset = Path(args.dataset)
    output_dir = Path(args.output)

    output_dir.mkdir(parents=True, exist_ok=True)

    unzipped_data_files = [dataset.joinpath(f) for f in listdir(dataset) if dataset.joinpath(f).exists()]

    # TODO: parallelize me!

    for tif_file in tqdm(unzipped_data_files):

        output_file = output_dir.joinpath(tif_file.stem).with_suffix(".npy")

        if not output_file.exists():

            img = read_tiff(tif_file)

            regions = extract_regions(img, args.size, args.stride)

            print(f"Extracted images: {len(regions)}")
            
            np.save(output_file, regions)