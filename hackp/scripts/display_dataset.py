import numpy as np
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt


if __name__=='__main__':

    regions = np.load("/shared_volume/npy/F16_042066_1532_XN_26S322W.cal.npy")

    size = 1024

    print(f"Regions shape: {regions.shape}")

    for i, region in enumerate(regions[0:20]):
        plt.figure()
        ax = plt.subplot()
        ax.imshow(region.reshape(size,size), cmap="magma")
        plt.savefig(f"{i}.png")
    