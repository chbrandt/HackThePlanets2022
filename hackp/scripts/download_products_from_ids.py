import os
import shutil
import argparse
from tqdm import tqdm 
from pathlib import Path
from time import strftime
from multiprocessing import Process

import adamapi
from adamapi import Auth
from adamapi import Search
from adamapi import GetData
from adamapi import Datasets

def auth(token):
    a = Auth()
    if "ADAM_API_KEY" not in os.environ and not token: 
        raise ValueError("Export ADAM_API_KEY or pass --token")
    if "ADAM_API_KEY" in os.environ:
        a.setKey(os.environ["ADAM_API_KEY"])
    if args.token:
        a.setKey(token)
    a.setAdamCore("https://explorer-space.adamplatform.eu")
    a.authorize()
    return a

def get_adam_data_service(auth):
    return GetData(auth)

def parse_products_ids_file(ids_file):
    with open(ids_file, "r") as pf:
        products_ids = [pid.rstrip('\n') for pid in pf.readlines()]
        return products_ids

def extract_zip(output_dir, zip_file):

    unzipped_datafile = output_dir.joinpath(zip_file.stem)
    
    if not unzipped_datafile.exists():
        print(f"Unzipping {zip_file}..")
        shutil.unpack_archive(zip_file, output_dir)
        print(f"Deleting {zip_file}..")
        zip_file.unlink()
    else:
        print(f"Unzipped file already exists: {unzipped_datafile}")


if __name__=='__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file-ids", type=str, required=True, help='The path to a file containing the products ids')
    parser.add_argument("-o", "--output", type=str, required=True, help='The path to an output directory that will contain the output files')
    parser.add_argument("-t", "--token", type=str, required=False, default="", help='The adamapi toker')
    parser.add_argument("-dsid", "--dataset-id", type=str, required=False, default="58592:MRO_CTX", help='The dataset id')

    args = parser.parse_args()

    adam_data_service = get_adam_data_service(auth(args.token))

    tmp_dir = Path(f'/tmp/adam_zip_{strftime("%Y%m%d-%H%M%S")}')
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    processes = []
    for product_id in tqdm(parse_products_ids_file(args.file_ids)):
        
        output_filename = tmp_dir.joinpath(product_id).with_suffix(".tif.zip")
        
        if not output_filename.exists():

            try:
                print(f"Downloading {product_id} to {output_filename}")
                adam_data_service.getData(args.dataset_id, productId = product_id, outputFname=output_filename)
                #p = Process(target=extract_zip, args=(output_dir,output_filename))
                #p.start()
                #processes.append(p)

            except Exception as e:
                print(f"Product ID {product_id} is not found")
                print(e)
                continue

        else:
            print(f"File {output_filename} has already been downloaded...") 


    print("Waiting for all extracting-zip processes to finish..")
    for p in processes:
        p.join()
