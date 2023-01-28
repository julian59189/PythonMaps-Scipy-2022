# This tutorial shows how to simply plot points on a world map

1. Select a datasource that you would like to plot. E.g. Captials. You can find an example in `resources/julian/capitals/`
1. Read the data into a Pandas dataframe and inspect. Make sure you chose the correct delimiter
    ```python
    file = 'resources/julian/capitals/data.csv'
    df = pd.read_csv(file, delimiter="\t")
    print(df)
    ```
1. Convert your data into the correct format. `GeoDataFrame` wants longitude and latitude values as floats. You can define your own convert function to parse your locations
    ```python
    # In:  Andorra  Andorra la Vella  42°31'N   01°32'E
    # Out: Andorra  Andorra la Vella  1.533333  42.516667
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
    ```
1. Create Points and GeoDataFrame
    ```python
    capital_geometry = [Point(xy) for xy in zip(df['lon'], df['lat'])]
    gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.lon, df.lat))
    ```
1. Get a reference map to plot on
    ```python
    world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
    ```
1. Plot GeoDataFrame
    ```python
    gdf.plot(ax=ax, color='red', markersize=1)
    plt.show()
    ```
1. You can also add more information/attributes to map e.g. names. You can plot any kind of string in colum of dataframe. Just inspect your pandas dataframe and pick column by name
    ```python
    for x, y, label in zip(gdf.geometry.x, gdf.geometry.y, gdf.Capital):
    ax.annotate(label, xy=(x, y), xytext=(3, 3), textcoords="offset points")
    ```