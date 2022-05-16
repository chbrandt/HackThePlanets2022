import rasterio
import numpy as np
import tensorflow as tf
from tensorflow.image import extract_patches

def read_tiff(filepath):
    img = None
    with rasterio.open(filepath) as tif:
        img = tif.read(1)
        img[img<=tif.nodata] = np.nan
    return img

def extract_regions(img, region_size, stride):

    #print(f"Shape of image: {img.shape}")

    if len(img.shape) == 2:
        img = np.expand_dims(img, axis=0)
        img = np.expand_dims(img, axis=-1)

    #print(f"New shape of image: {img.shape}")

    sizes = [1, region_size, region_size, 1]
    depth = img.shape[3]

    patches = extract_patches(images=img,
                    sizes=[1,region_size,region_size,1],
                    strides=[1, stride, stride, 1],
                    rates=[1, 1, 1, 1],
                    padding='VALID')
    
    # (1, 30, 9, 1048576) => (30, 9, 1048576) => (270, 1048576)
    patches = np.squeeze(patches.numpy(), axis=0)
    
    patches = patches.reshape(patches.shape[0]*patches.shape[1], patches.shape[2])
    
    #print(f"Region shapes: {patches.shape}")
    
    to_delete = []
    count_ok = 0
    for i, r in enumerate(patches):
        if np.isnan(r).any():
            to_delete.append(i)
        else:
            count_ok += 1
            
    #print(f"Not ok: {len(to_delete)}")
    #print(f"Ok: {count_ok}")
    
    regions = np.delete(patches, to_delete, axis=0)
    
    #print(f"After deletion: {regions.shape}")
    
    return regions