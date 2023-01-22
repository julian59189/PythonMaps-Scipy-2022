
import csv
import matplotlib.pyplot as plt
import pandas as pd
from shapely.geometry import Point
import geopandas as gpd
from dataprep.clean import clean_lat_long

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
capital_geodata = gpd.GeoDataFrame(df, 
                                crs="EPSG:4326", 
                                geometry=capital_geometry)

fig, ax = plt.subplots(figsize=(10,5))
capital_geodata.plot(ax=ax)
plt.show()

# s = "34°28'N"
# out = s.split("°")
# h = int(out[0])
# print(out)
# out2 = out[1].split("'") 
# m = int(out2[0])
# dir = out2[1]
# print("h: {} m: {} dir: {}".format(h,m,dir))