import numpy as np
from tqdm import tqdm
from os import listdir
from pathlib import Path

from hackp.utils.imgproc import read_tiff, extract_regions

if __name__=='__main__':

    # TODO: datapath, outputpath, size and stride as input args

    datapath_unzipped = Path("/shared_volume/unzipped")
    datapath_npy = Path("/shared_volume/npy")
    size = 1024
    stride = 1024

    datapath_npy.mkdir(parents=True, exist_ok=True)

    unzipped_data_files = [datapath_unzipped.joinpath(f) for f in listdir(datapath_unzipped) if datapath_unzipped.joinpath(f).exists()]

    # TODO: parallelize me!

    for tif_file in tqdm(unzipped_data_files):

        output_file = datapath_npy.joinpath(tif_file.stem).with_suffix(".npy")

        if not output_file.exists():

            img = read_tiff(tif_file)

            regions = extract_regions(img, size, stride)

            print(f"Extracted images: {len(regions)}")
            
            np.save(output_file, regions)