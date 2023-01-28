
import csv
import matplotlib.pyplot as plt
import pandas as pd
from shapely.geometry import Point
import geopandas as gpd
from dataprep.clean import clean_lat_long

import matplotlib.ticker as mticker
import cartopy.crs as ccrs

from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER

def get_capital_geometry():
    # opening the CSV file
    file = 'resources/julian/capitals/data.csv'
    df = pd.read_csv(file, delimiter="\t")
    print(df)

    # from: https://stackoverflow.com/questions/21298772/how-to-convert-latitude-longitude-to-decimal-in-python
    # 20-55-70.010N: 20.9361138889
    # 32-11-50.000W: -32.1972222222
    def convert(tude):
        out = tude.split("°")
        h = int(out[0])
        out2 = out[1].split("'") 
        m = int(out2[0])
        dir = out2[1]
        multiplier = 1 if dir in ['N', 'E'] else -1
        return multiplier * (float(h) + float(m)/60)

    df['lon'] = df["Longitude"].map(convert)
    df['lat'] = df["Latitude"].map(convert)
    print(df)
    capital_geometry = [Point(xy) for xy in zip(df['lon'], df['lat'])]
    return df, capital_geometry


# main part
df, capital_geometry = get_capital_geometry()

# print(capital_geometry)

# # pack them into GeoDataFrame
# port_geodata = gpd.GeoDataFrame(df, 
#                                 crs="EPSG:4326", 
#                                 geometry=capital_geometry)

# # plot airports
# fig, ax = plt.subplots(facecolor='black', 
#                        subplot_kw={'projection': ccrs.Robinson()}, 
#                        figsize=(10,5))
# ax.patch.set_facecolor('black')


# port_geodata.plot(ax=ax, transform=ccrs.PlateCarree(), 
#                      markersize=4, alpha=1, color='crimson', 
#                      edgecolors='none')
# plt.setp(ax.spines.values(), color='black')
# plt.setp([ax.get_xticklines(), ax.get_yticklines()], color='black')
# ax.set_ylim(-7000000, 9000000)
# plt.show()


# # gdf = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))


# # # plt.figure(figsize=(10, 5))
# # fig, ax = plt.subplots(subplot_kw={'projection': ccrs.Robinson()}, 
# #                        figsize=(10,5))
# # ax = plt.axes(projection=ccrs.LambertCylindrical())
# # gdf.plot(ax=ax, transform=ccrs.PlateCarree())
# # gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True,
# #                   linewidth=2, color='black', alpha=0.5, linestyle='--')
# # # plt.show()

# # capital_geodata = gpd.GeoDataFrame(df, 
# #                                 crs="EPSG:4326", 
# #                                 geometry=capital_geometry)
# # plt.setp(ax.spines.values(), color='black')

# # # fig, ax = plt.subplots(figsize=(10,5))
# # capital_geodata.plot(ax=ax, color='darkviolet')
# # plt.show()


# df = pd.DataFrame(
#     {'City': ['Buenos Aires', 'Brasilia', 'Santiago', 'Bogota', 'Caracas'],
#      'Country': ['Argentina', 'Brazil', 'Chile', 'Colombia', 'Venezuela'],
#      'Latitude': [-34.58, -15.78, -33.45, 4.60, 10.48],
#      'Longitude': [-58.66, -47.91, -70.66, -74.08, -66.86]})

gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.lon, df.lat))

world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

# We restrict to South America.
ax = world.plot(
    color='white', edgecolor='black')

# ax = world[world.continent == 'South America'].plot(
#     color='white', edgecolor='black')

# We can now plot our ``GeoDataFrame``.
gdf.plot(ax=ax, color='red', markersize=1)

for x, y, label in zip(gdf.geometry.x, gdf.geometry.y, gdf.Capital):
    ax.annotate(label, xy=(x, y), xytext=(3, 3), textcoords="offset points")

plt.show()