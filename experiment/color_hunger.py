import matplotlib.pyplot as plt
import geopandas as gpd
from descartes import PolygonPatch
import pandas as pd 
import matplotlib.cm as cm
import matplotlib as matplotlib
import util.util as util

# read in world map
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
# plot the whole world
#ax2 = world.plot( figsize=(8,4), edgecolor=u'gray', cmap='Set2' )
afrika = world[world.continent == 'Africa']

# or plot Africa continent
ax2 = afrika.plot(figsize=(8,8), edgecolor=u'gray', cmap='gray')
# reduce contries to africa



file = 'resources/julian/hunger/data.csv'
df = pd.read_csv(file, delimiter="\t")
# filter to only africa
df =  df[df['Continent'].str.contains('Africa', na=False)]

def plotCountryPatch(axes, country_name, fcolor):
    # plot a country on the provided axes
    try:
        nami = world[world.name == country_name.strip()]
        namigm = nami.__geo_interface__['features']  # geopandas's geo_interface
        namig0 = {'type': namigm[0]['geometry']['type'], \
                'coordinates': namigm[0]['geometry']['coordinates']}
        axes.add_patch(PolygonPatch( namig0, fc=fcolor, ec="black", alpha=0.85, zorder=2 ))
        # print(country_name, ": exists")
    except:
        print(country_name, ": does NOT exist")


# exit()
# paint all countries with single color
for f in afrika.name:
    # print("country: ", f)
    # print(type(f))
    o = f.split(": ")[-1]
    # print("c:[", o, "]")
    plotCountryPatch(ax2, o, "gray")


# print("max val: ", df['2022'].min())
# todo: make max work

# annotate
afrika['coords'] = afrika['geometry'].apply(lambda x: x.representative_point().coords[:])

afrika['coords'] = [coords[0] for coords in afrika['coords']]
# fig, ax = plt.subplots(figsize = (10,10))
# gdf_swk.plot(ax=ax, color=’yellow’, edgecolor=’black’)
for idx, row in afrika.iterrows():
   ax2.annotate(text=row['name'], xy=row['coords'], horizontalalignment='center', color='blue')


# colorcode countries
maxval = 20
for ind in df.index:
    col = util.int_to_color(df['2022'][ind], maxval)
    country = df['Country'][ind]
    country = country.split("(")[0]
    plotCountryPatch(ax2, country, col)
    # print("{}: val: {}".format(country, df['2022'][ind]))

# then plot some countries on top
# plotCountryPatch(ax2, 'Uganda', 'gray')


plt.ylabel('Latitude')
plt.xlabel('Longitude')

#ax2.axis('scaled')
plt.show()