import shutil
import argparse
import multiprocessing
from pathlib import Path


def extract_zip(output_dir, zip_file):

    unzipped_datafile = output_dir.joinpath(zip_file.stem)

    if not unzipped_datafile.exists():
        print(f"Unzipping {zip_file}..")
        shutil.unpack_archive(zip_file, output_dir)
    else:
        print(f"Unzipped file already exists: {unzipped_datafile}")

if __name__=="__main__":

    tmp_dir = Path("/home/baroncelli/HackThePlanetsDataset/tif_zip")
    datapath_unzipped = Path("/home/baroncelli/HackThePlanetsDataset/tif")

    datapath_unzipped.mkdir(exist_ok=True, parents=True)

    zipped_data_files = [tmp_dir.joinpath(f) for f in os.listdir(tmp_dir) if tmp_dir.joinpath(f).exists() and ".tif.zip" in f]

    pool = multiprocessing.Pool(processes=120)

    pool.map(partial(extract_zip, datapath_unzipped), zipped_data_files)
