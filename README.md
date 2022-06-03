# Hack the planets 2022
## Table of contents
- [Hack the planets 2022](#hack-the-planets-2022)
  - [Table of contents](#table-of-contents)
  - [Docker image](#docker-image)
  - [Dataset generation](#dataset-generation)
    - [Dataset 'craters'](#dataset-craters)
  - [Models](#models)
    - [StyleGAN2-ADA - ppc64le (POWER9)](#stylegan2-ada---ppc64le-power9)
      - [Dataset for StyleGAN2-ADA](#dataset-for-stylegan2-ada)
      - [Training](#training)
      - [Tensorboard](#tensorboard)
      - [Workarounds](#workarounds)
      - [Results](#results)
## Docker image

You can build a docker image that provides an Ubuntu OS with python 3.8 and the adamapi python library.

Build the image with:
```
cd adamapi_docker
docker build --no-cache --network=host --tag adamapiimg:latest .
```
Start a jupyter server inside a new container:
```
export SHARED_VOLUME=/data/datasets/hack_the_planets
./start_notebook.sh
```
Start a shell inside a new container:
```
./start_container.sh
export PYTHONPATH=/shared_dir
```

## Dataset generation

1. Use the script 'download_products_from_ids.py' script to download the tif files. The input is a .txt file containing the products ids you want to download.
```
cd hackp/scripts
python download_products_from_ids.py -f /shared_dir/data/craters_dataset.txt -o /shared_volume/tif_craters -t <apikey> -dsid 58592:MRO_CTX
```
2. Use the 'create_dataset.py' script to generate the images for the training in .npy format.
3. You can use the 'display_dataset.py' script to generate some .png previews of those images.

### Dataset 'craters'
The 56 products that compose this dataset can be found in data/craters_dataset.txt

From those tif files, the following datasets have been generated:

| Resolution | Stride | Number of files | Total memory | Location                                           |
|------------|--------|-----------------|--------------|----------------------------------------------------|
| 128x128    | 128    | 529787          | 35GB         | agilehost3:/scratch/hacktheplanets/craters-npy-128 |
| 256x256    | 256    | 127683          | 32GB         | agilehost3:/scratch/hacktheplanets/craters-npy-256 |
| 512x512    | 256    | 118411          | 117GB        | ibmtest:/scratch/hack_the_planets/craters-npy-512-256st    |
| 1024x1024  | 1024   | 6212            | 25GB         | ibmtest:/scratch/hack_the_planets/craters-npy-1024         |
## Models
### StyleGAN2-ADA - ppc64le (POWER9)
The NVIDIA StyleGAN2-ADA repository has been forked, and adapted to work with a
power9 machine.

Checkout the power9 branch and create an anaconda environment with:
```
cd stylegan2-ada-fork
conda env create --file environment.yml
```
#### Dataset for StyleGAN2-ADA
The .npy dataset [must be converted into multi-resolution TFRecords](https://github.com/LeoBaro/stylegan2-ada/tree/3bba7a31472ec69cbc1475d6529a8614206ded2a#preparing-datasets). 
The dataset_tool.py script has been modified to be able to process .npy data and to
write preview of the generated images in the .png format (instead of showing them with opencv).
```
python dataset_tool.py create_from_npy /scratch/hack_the_planets/craters-multi-res-1024 /scratch/hack_the_planets/craters-npy-1024 1024
python dataset_tool.py png_preview /scratch/hack_the_planets/craters-multi-res-1024
```

#### Training
The training can be started **from scratch on ibmtest** with:
```
cd stylegan2-ada-fork
conda activate stylegan2ada
source ../load_nvcc.sh
module load gcc-8.5.0
nohup python train.py --outdir=./training-runs --gpus=2 --data=/scratch/hack_the_planets/craters-multi-res-512-256st --mirror=1 --cfg=stylegan2 --snap=10 > train_512sz_256st.log 2>&1 &
```
Check the [StyleGAN2-ada README.md](https://github.com/LeoBaro/stylegan2-ada/tree/3bba7a31472ec69cbc1475d6529a8614206ded2a#training-new-networks) for other details.

If you want to restore a training, add the following input parameter:
```
--resume=~/training-runs/<RUN_NAME>/network-snapshot-<KIMG>.pkl
```

#### Tensorboard
On the remote machine:
```
cd stylegan2-ada-fork/training-runs/00003-craters-multi-res-1024-mirror-stylegan2
nohup tensorboard --logdir ./ --port 6006 > tensorboard.log 2>&1 &
```
On the local machine:
```
ssh -N -L localhost:16006:localhost:6006 <username>@<remote_machine_dns_name>
```

#### Workarounds
The original code has been modified, to workaround some issues.
1. The following nvcc compiler flag has been added at row 143 of dnnlib/tflib/custom_ops.py
```
compile_opts += " -Xcompiler -mno-float128 "
```
This will overcome a compilation error (__ieee128 is undefined).

2. The following instruction has been added at row 81 of training_loop.py to reduce the number of the images dimension.
```
images = np.squeeze(images, axis=2)
```
This will overcome a runtime error.

#### Experiments

Model for 512 resolution images. Models and logs:
* 00005-craters-multi-res-512-256st-mirror-stylegan2
* 00006-craters-multi-res-512-256st-mirror-stylegan2-resumecustom
![StyleGAN2-ADA (512x512) Generator](assets/img/stylega2-ada-512-res-fakes001228.png)

Model for 1024 resolution images. Models and logs:
* 00007-craters-multi-res-1024-mirror-stylegan2
![StyleGAN2-ADA (1024x1024) Generator](assets/img/stylega2-ada-1024-res-fakes000778.png)