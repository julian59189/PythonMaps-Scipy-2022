import matplotlib.ticker as mticker
import cartopy.crs as ccrs

from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
import matplotlib.pyplot as plt
import geopandas as gpd

import geopandas as gpd
import pandas as pd
from shapely.geometry import Point
from shapely.geometry import LineString
from shapely.geometry import Polygon

points = [Point(-4, 0.), Point(-5, 12.),Point(-6., 3.),Point(-8., 7.),Point(-4., 8.),Point(-3., 2.),Point(-1., 6.)]

points_gdf = gpd.GeoDataFrame(pd.DataFrame({'Name': ["P1","P2","P3","P4","P5","P6","P7"]}), 
                              crs="EPSG:4326", 
                              geometry=points)

Lines = [LineString([Point(-4, 0.), Point(-5, 12.), Point(-6., 3.)]),
         LineString([Point(-8., 7.),Point(-4., 8.),Point(-3., 2.),Point(-1., 6.)])]

lines_gdf = gpd.GeoDataFrame(pd.DataFrame({'Name': ["Line 1", "Line 2"]}), 
                             crs="EPSG:4326", 
                             geometry=Lines)

geoms = Polygon([(0,0),(0,5),(5,5),(5,0),(0,0)])
polygon_gdf = gpd.GeoDataFrame(pd.DataFrame({'Name': ["Polygon"]}), 
                               crs="EPSG:4326", 
                               geometry=[geoms])

gdf = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

# gdf = pd.concat([points_gdf, lines_gdf, polygon_gdf]).reset_index(drop=True)
# gdf["area"] = gdf.area
# gdf['boundary'] = gdf.boundary
# gdf['centroid'] = gdf.centroid

# print(gdf)

# ax = plt.axes(projection=ccrs.Mercator())
# gdf.plot(ax=ax, transform=ccrs.PlateCarree())
# gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True,
#                   linewidth=2, color='black', alpha=0.5, linestyle='--')
# plt.show()

# ax = plt.axes(projection=ccrs.LambertCylindrical())
# gdf.plot(ax=ax, transform=ccrs.PlateCarree())
# gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True,
#                   linewidth=2, color='black', alpha=0.5, linestyle='--')
# plt.show()

import matplotlib.ticker as mticker
import cartopy.crs as ccrs

from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER

plt.figure(figsize=(10, 5))
ax = plt.axes(projection=ccrs.Mercator())
gdf.plot(ax=ax, transform=ccrs.PlateCarree())
gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True,
                  linewidth=2, color='black', alpha=0.5, linestyle='--')
plt.show()