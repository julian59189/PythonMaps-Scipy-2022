# following: https://towardsdatascience.com/creating-beautiful-topography-maps-with-python-efced5507aa3

import rasterio
import matplotlib.pyplot as plt
import cartopy
import cartopy.crs as ccrs
file = rasterio.open('data/30N000E_20101117_gmted_mea075.tif')
dataset = file.read()
print(dataset.shape)

plt.imshow(dataset[0], cmap='Spectral')
plt.show()

import geopandas as gpd
from shapely.geometry import mapping
from rasterio import mask as msk

df = gpd.read_file('NaturalEarth/data/10m_cultural/ne_10m_admin_0_countries.shp')

italy = df.loc[df['ADMIN'] == 'Italy']

clipped_array, clipped_transform = msk.mask(file, [mapping(italy.iloc[0].geometry)], crop=True)

plt.imshow(clipped_array[0], cmap='Spectral')
plt.show()