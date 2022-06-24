import os
import logging
import argparse
import numpy as np
from time import time
from PIL import Image
from os import listdir
import multiprocessing
from pathlib import Path
from functools import partial 

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
from hackp.utils.tif import read_tif
from hackp.utils.imgproc import extract_regions, linear_stretch

def save_img(img, output_dir, filename, save_jpg=False):

    output_file = output_dir.joinpath(filename).with_suffix(".npy")
    
    if not output_file.exists():
        np.save(output_file, img)
        
    if save_jpg:
        output_file = output_dir.joinpath(filename).with_suffix(".jpg")
        im = Image.fromarray(np.squeeze(img, axis=-1)).convert("L")
        im.save(output_file)

    return True 
    
def extract_patch_and_save(output_dir, tif_file):

        pid = multiprocessing.current_process().name

        logging.info(f"{pid} - Opening and extracting images from: {tif_file.stem}")

        start_t = time()

        try:
            regions = np.expand_dims(
                np.apply_along_axis(
                    linear_stretch, 1, 
                        extract_regions(read_tif(tif_file), args.size, args.stride))
                            .reshape(-1, args.size, args.size), axis=-1) # => (N,H,W,C)

        except Exception as e:    
            logging.error(f"{pid} - Exception during reading tif and images extraction:\n\n{e}")
            return 0

        tf_time = time() - start_t
        logging.info(f"{pid} - Extracted images: {regions.shape}. Took {round(tf_time,2)}s. Writing the images on disk..") # (N, H, W)

        start_t = time()
        count = 0
        for idx,region in enumerate(regions):
            if save_img(region, output_dir, tif_file.stem+f"_{idx}"):
                count += 1

        w_time = time() - start_t
        logging.info(f"{pid} - Wrote {count} images. Writing took: {round(w_time,2)}s.")

        return regions.shape[0]



if __name__=='__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--dataset", type=str, required=True, help='The path to an input direcotry containing .tif files')
    parser.add_argument("-o", "--output", type=str, required=True, help='The path to an output direcotry that will contain the output files')
    parser.add_argument("-sz", "--size", type=int, required=True, help='The size of the square images that are going to be extracted')
    parser.add_argument("-st", "--stride", type=int, required=True, help='If stride==size, there will be no overlapping')
    parser.add_argument("-j", "--jobs", type=int, required=False, default=2, help="The number of worker reader threads")
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    dataset = Path(args.dataset)

    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)


    """
    logging.info('Reading the output directory..')
    groups = defaultdict(list)
    for filename in os.listdir(output_dir):
        keyname = filename.rsplit("_", 1)[0]
        if keyname in groups:
            groups[keyname].append(filename)
        else:
            groups[keyname] = []

    for filename, count in groups.items():
        print(f"{filename} = {count}")
    """

    unzipped_data_files = [dataset.joinpath(f) for f in listdir(dataset) if dataset.joinpath(f).exists()]


    if args.jobs > 0:
        results = []
        with multiprocessing.Pool(processes=args.jobs) as pool:
            for result in pool.imap(partial(extract_patch_and_save, output_dir), unzipped_data_files):
                results.append(result)
            pool.close()
            pool.join()
        print(f"Total files produced: {sum(results)}")

    else:
        for unzipped_data_file in unzipped_data_files:
            extract_patch_and_save(output_dir, unzipped_data_file)