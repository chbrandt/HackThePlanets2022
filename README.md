# Hack the planets 2022

## Docker container
```
cd adamapi_docker
./start_container.sh
export PYTHONPATH=/shared_dir
```
## Dataset generation

1. Use the notebook 'download_products_from_ids.py' script to download the tif files.
```
cd hackp/scripts
python download_products_from_ids.py -f /shared_dir/data/craters_dataset.txt -o /shared_volume/tif_craters -t <apikey> -dsid 58592:MRO_CTX
```
2. Use the 'create_dataset' script to generate the images for the training in .npy format.
3. You can use the 'display_dataset' script to generate some png previews of those images.

### Dataset craters
The 56 products that compose this dataset can be found in data/craters_dataset.txt

From those tif files, the following datasets have been generated:
* 128x128 resolution (stride=128), 529787 .npy files, 35G of size, agilehost3:/scratch/hacktheplanets
* 256x256 resolution (stride=256), 127683 .npy files, 32GB of size, agilehost3:/scratch/hacktheplanets
* 512x512 resolution (stride=256), 118411.npy files, of size, morgana:/data01/hacktheplanets
* 1024x1024 resolution (stride=1024), 6212 .npy files, 25GB of size, ibmtest:/scratch/hacktheplanets

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
The dataset_tool.py script has been modified to be able to process .npy data and to
write preview of the generated images in the .png format (instead of showing them with opencv).
```
python dataset_tool.py create_from_npy /scratch/hack_the_planets/craters-multi-res-1024 /scratch/hack_the_planets/craters-npy-1024 1024
python dataset_tool.py png_preview /scratch/hack_the_planets/craters-multi-res-1024
```

#### Training
The training can be started *from scratch* with:
```
conda activate stylegan2ada
source ../load_nvcc.sh
module load gcc-8.5.0
nohup python train.py --outdir=./training-runs --gpus=2 --data=/scratch/hack_the_planets/craters-multi-res-512-256st --mirror=1 --cfg=stylegan2 --snap=10 > train_512sz_256st.log 2>&1 &
```
Check the StyleGAN2-ada README.md for other details.

If you want to restore a training:
```
--resume=ffhq1024 --snap=10
```

#### Tensorboard
On the remote machine:
```
cd stylegan2-ada-fork/training-runs/00003-craters-multi-res-1024-mirror-stylegan2
nohup tensorboard --logdir ./ --port 6006 > tensorboard.log 2>&1 &
```
On the local machine:
```
ssh -N -L localhost:16006:localhost:6006 baroncelli@ibmtest.iasfbo.inaf.it
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
