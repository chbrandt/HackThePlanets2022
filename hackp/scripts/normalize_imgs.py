import argparse
from pathlib import Path
import numpy as np
from os import listdir
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable

def print_img_range(images):
    for i in range(3):
        max = images[i,:,:].max()
        min = images[i,:,:].min()
        print(f"Imgs range: {min} - {max} ")

def export_imgs(images, filename_suffix, output_dir):
    fig, ax = plt.subplots(3, 1, figsize=(10,10))
    ax = ax.ravel()
    for i in range(0, 3):
        #img = images[0].transpose(1, 2, 0)[:, :, ::-1]
        img = images[i]
        print(img.shape)
        imm = ax[i].imshow(img, cmap='Greys')
        divider = make_axes_locatable(ax[i])
        cax = divider.append_axes('right', size='5%', pad=0.05)
        fig.colorbar(imm, cax=cax, orientation='vertical')

    output_file = output_dir.joinpath(f"{filename_suffix}.png")
    fig.savefig(output_file, dpi=300)

def linear_stretch(img, a, b):
    c = img.min()
    d = img.max()
    return (img-c) * ((b-a)/(d-c)) + a

if __name__=='__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--dataset", type=str, required=True, help='The path to an input direcotry containing .npy files')
    parser.add_argument("-o", "--output", type=str, required=True, help='The path to an output direcotry that will contain the output files')
    parser.add_argument("-sz", "--size", type=int, required=True, help='The size of the square images that are going to be extracted')
    args = parser.parse_args()

    dataset = Path(args.dataset)

    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    npy_images = np.squeeze(
                    np.stack(
                        [np.load(dataset.joinpath(df)).astype('float32') for df in listdir(args.dataset)],
                        axis=0),
                    axis=-1) # (N,H,W)
    print(f"Images shape: {npy_images.shape}")

    print_img_range(npy_images)
    export_imgs(npy_images, "not-norm", output_dir)

    npy_images_norm1 = npy_images * (255.0/npy_images.max())
    print_img_range(npy_images_norm1)
    export_imgs(npy_images_norm1, "norm", output_dir)

    for i in range(3):
        npy_images[i,:,:] = linear_stretch(npy_images[i,:,:], 0., 255.)
    print_img_range(npy_images)
    export_imgs(npy_images, "linear-stretch", output_dir)

    for i in range(3):
        npy_images[i,:,:] = linear_stretch(npy_images[i,:,:], 0, 255)
    npy_images = np.rint(npy_images).astype('int')
    print_img_range(npy_images)
    export_imgs(npy_images, "linear-stretch-asint", output_dir)
