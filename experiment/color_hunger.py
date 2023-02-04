import matplotlib.pyplot as plt
import geopandas as gpd
from descartes import PolygonPatch
import pandas as pd 
import matplotlib.cm as cm
import matplotlib as matplotlib
import util.util as util

def plot_afrika():
    # read in world map
    world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
    # plot the whole world
    #ax2 = world.plot( figsize=(8,4), edgecolor=u'gray', cmap='Set2' )
    afrika = world[world.continent == 'Africa']

    # or plot Africa continent
    ax2 = afrika.plot(figsize=(8,8), edgecolor=u'gray', cmap='gray')
    # reduce contries to africa

    # annotate
    afrika['coords'] = afrika['geometry'].apply(lambda x: x.representative_point().coords[:])

    afrika['coords'] = [coords[0] for coords in afrika['coords']]
    # fig, ax = plt.subplots(figsize = (10,10))
    # gdf_swk.plot(ax=ax, color=’yellow’, edgecolor=’black’)
    for idx, row in afrika.iterrows():
        ax2.annotate(text=row['name'], xy=row['coords'], horizontalalignment='center', color='black')
    return ax2, afrika, world


def create_dataframe():
    file = 'resources/julian/hunger/data.csv'
    df = pd.read_csv(file, delimiter="\t")
    # filter to only africa
    df =  df[df['Continent'].str.contains('Africa', na=False)]
    # convert index to float for easier use
    df['2022'] = df['2022'].astype(float)
 
    return df

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

# main program
ax2, afrika, world = plot_afrika()
df = create_dataframe()
max_val = df['2022'].max()


for f in afrika.name:
    country_name = f.split(": ")[-1]
    plotCountryPatch(ax2, country_name, "gray")
    # check if country is in list
    in_list = df.Country.str.contains(country_name)
    if any(in_list):
        # get column index of country
        country_index = in_list.loc[lambda s_: s_].index[0]

        # get index
        hunger_index = df['2022'][country_index]

        if hunger_index > 0.01:
            col = util.int_to_color(hunger_index, max_val)
            country = df['Country'][country_index]
            country = country.split("(")[0]
            plotCountryPatch(ax2, country_name, col)
    # else:
    #     print("DIDNT find: ", country_name)

# then plot some countries on top
# plotCountryPatch(ax2, 'Uganda', 'gray')


plt.ylabel('Latitude')
plt.xlabel('Longitude')

#ax2.axis('scaled')
plt.show()