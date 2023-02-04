import matplotlib.pyplot as plt
import geopandas as gpd
from descartes import PolygonPatch
import pandas as pd 
import matplotlib.cm as cm
import matplotlib as matplotlib

world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
print(world)

file = 'resources/julian/hunger/data.csv'
df = pd.read_csv(file, delimiter="\t")

# print(df)
# filter to only africa
df =  df[df['Continent'].str.contains('Africa', na=False)]
# print(df)

# from  matplotlib.colors import LinearSegmentedColormap
# cmap=LinearSegmentedColormap.from_list('rg',["r", "w", "g"], N=256) 


def color_map_color(value, cmap_name='RdYlGn', vmin=0, vmax=1):
    # norm = plt.Normalize(vmin, vmax)
    norm = matplotlib.colors.Normalize(vmin=vmin, vmax=vmax)
    cmap = cm.get_cmap(cmap_name)  # PiYG
    cmap = cmap.reversed()
    rgb = cmap(norm(abs(value)))[:3]  # will return rgba, we take only first 3 so we get rgb
    color = matplotlib.colors.rgb2hex(rgb)
    return color

def int_to_color(value, maxval):
    try:
        # int_value = float(value)
        # print("cval: ", float(value))
        return color_map_color(float(value), vmin=0, vmax=maxval)
    except (TypeError, ValueError):
        # print('Not an integer: ', TypeError)
        # print('Not an integer: ', ValueError)
        return 'gray'

# print(world.name)

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

# plot the whole world
#ax2 = world.plot( figsize=(8,4), edgecolor=u'gray', cmap='Set2' )

# or plot Africa continent
ax2 = world[world.continent == 'Africa'].plot(figsize=(8,8), edgecolor=u'gray', cmap='gray')

# print(color_map_color(0, vmin=0, vmax=100))

# reduce contries to africa
afrika = world[world.continent == 'Africa']
# afrika['coords'] = afrika['geometry'].apply(lambda x: x.representative_point().coords[:])

# df.apply(lambda x: ax2.annotate(text=afrika['name'], xy=afrika.geometry.centroid.coords[0], ha='center'), axis=1)

# afrika.apply(lambda x: ax2.annotate(s=x.name, xy=x.geometry.centroid.coords[0], ha='center', fontsize=14),axis=1)
# # afrika.boundary.plot(ax=ax2, color='Black', linewidth=.4)
# # afrika.plot(ax=ax2, cmap='Pastel2', figsize=(12, 12))
# ax2.text(-0.05, 0.5, 'https://jcutrer.com', transform=ax2.transAxes,
#         fontsize=20, color='gray', alpha=0.5,
#         ha='center', va='center', rotation='90')
# print(afrika)
# print(type(afrika))

# exit()
# paint all countries with single color
for f in afrika.name:
    print("country: ", f)
    # print(type(f))
    o = f.split(": ")[-1]
    print("c:[", o, "]")
    plotCountryPatch(ax2, o, "gray")


# df.apply(lambda x: ax2.annotate(text=x['name'], xy=x.geometry.centroid.coords[0], ha='center'), axis=1)
    # ax2.text(f.lon - 1.5, f.lat, f.country, fontsize=5)
    # break
# exit()

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
    col = int_to_color(df['2022'][ind], maxval)
    country = df['Country'][ind]
    country = country.split("(")[0]
    plotCountryPatch(ax2, country, col)
    print("{}: val: {}".format(country, df['2022'][ind]))

# then plot some countries on top
# 
# plotCountryPatch(ax2, 'Uganda', 'gray')

# the place to plot additional vector data (points, lines)

plt.ylabel('Latitude')
plt.xlabel('Longitude')

#ax2.axis('scaled')
plt.show()