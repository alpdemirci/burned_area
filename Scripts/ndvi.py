# -*- coding: utf-8 -*-
"""
Created on Mon Jan 11 23:15:20 2021

@author: Alp

"""

import rasterio
from rasterio import plot
import matplotlib.pyplot as plt
import numpy as np


# Input data

band2 = rasterio.open('blue.img')           # Blue Band
band3 = rasterio.open('green.img')          # Green Band
band4 = rasterio.open('red.img')            # Red Band
band5 = rasterio.open('near_infrared.img')  # Near Infrared Band


# False Color Image
# -----------------------------------------------------------------------------
green = band3.read(1).astype('float64')
red = band4.read(1).astype('float64')
nir = band5.read(1).astype('float64')


def normalize(array):
    """
    Normalize the interval of the elements of the array between 0 and 1
    
    
    Parameters
    ----------
    array: type(array) size:999x999 cells include pixel reflectance values
    float id
    
    
    Returns
    -------
    norm_array : type(array) size:999x999 cells include pixel reflectance values
    as normalized values

    """
    array_min, array_max = array.min(), array.max()
    return ((array - array_min)/(array_max - array_min))

# Normalize the bands


redn = normalize(red)
greenn = normalize(green)
nirn = normalize(nir)
false_color = np.dstack((nirn, redn, greenn))
plt.imshow(false_color)


# -----------------------------------------------


# True Color Image
# -----------------------------------------------
blue = band2.read(1).astype('float64')
green = band3.read(1).astype('float64')
red = band4.read(1).astype('float64')

bluen = normalize(blue)

true_color = np.dstack((bluen, redn, greenn))
plt.imshow(true_color)
# -----------------------------------------------
# NDVI Calculation
ndvi = np.where((nir+red) == 0., 0, (nir - red) / (nir + red))
ndviImage = rasterio.open('ndviImage1.tiff', 'w', driver='Gtiff',
                          width=band4.width,
                          height=band4.height,
                          count=1, crs=band4.crs,
                          transform=band4.transform,
                          dtype='float64')
ndviImage.write(ndvi, 1)
ndviImage.close()
# plot ndvi
ndvi = rasterio.open('ndviImage1.tiff')
fig = plt.figure(figsize=(18, 12))
plot.show(ndvi)
# ----------------------------------------------
