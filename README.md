# Hack the planets 2022

## Dataset generation

1. Use the notebook 'adam_api_example' to download the tif files.
2. Use the 'create_dataset' script to generate the images for the training in .npy format.
3. You can use the 'display_dataset' script to generate some png previews of those images.

### Dataset craters
<<<<<<< Updated upstream
The 56 products that compose this dataset can be found in data/craters_dataset.txt

From those tif files, the following datasets have been generated:
* Res: 127683 .npy files, 256x256 resolution, 32GB of size.
* Res: ? .npy files, 1024x1024 resolution, 25GB of size.
=======
>>>>>>> Stashed changes

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
python dataset_tool.py create_from_npy ~/HackThePlanetsDataset/multi-res-1024 /scratch/hack_the_planets/craters-npy-1024 1024
python dataset_tool.py display ~/HackThePlanetsDataset/multi-res-1024/
```

#### Training
The training can be started with:
```
source ../load_nvcc.sh
module load gcc-8.5.0
python train.py --outdir=./training-runs --gpus=2 --data=./HackThePlanetsDataset/multi-res-1024 --mirror=1 --cfg=stylegan2 --snap=10
```
Check the StyleGAN2-ada README.md for other details.

#### Workarounds
The original code has been modified, to workaround some issues.
1. The following nvcc compiler flag has been added at row 143 of dnnlib/tflib/custom_ops.py
```
compile_opts += " -Xcompiler -mno-float128 "
```
This will overcome a compilation error.

2. The following instruction has been added at row 81 of training_loop.py to reduce the number of the images dimension.
```
images = np.squeeze(images, axis=2)
```
This will overcome a runtime error.
