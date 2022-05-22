import rasterio

def read_tif(filepath):
    img = None
    with rasterio.open(filepath) as tif:
        img = tif.read(1)
        img[img<=tif.nodata] = np.nan
    return img
