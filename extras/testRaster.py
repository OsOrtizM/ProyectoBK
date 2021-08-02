import numpy
import rasterio
from rasterio.windows import Window

image = numpy.ones((3601, 3601), dtype=rasterio.ubyte) * 127

with rasterio.open(
        'img/ASTER-GDEM-BOLIVIA/Data/ASTGTM2_S18W067_dem_test.tif', 'w',
        driver='GTiff', width=3061, height=3601, count=1,
        dtype=image.dtype) as dst:
    print(dst) # dst.write(image, window=Window(50, 30, 3061, 3061), indexes=1)