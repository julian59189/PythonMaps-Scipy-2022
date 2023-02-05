import geopandas as gpd
import matplotlib.pyplot as plt
import cartopy.crs as ccrs

roman_empire = gpd.read_file("resources/roman_empire.geojson")
mongol_empire = gpd.read_file("resources/mongol_empire.geojson")
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
overlap = roman_empire.overlay(mongol_empire, how='intersection')

fig, ax2 = plt.subplots(subplot_kw={'projection': ccrs.Mercator()}, 
                       figsize=(10,10))

world.plot(ax=ax2, 
                   transform=ccrs.PlateCarree(), 
                   color='gray')

roman_empire.plot(ax=ax2, 
                  transform=ccrs.PlateCarree(), 
                  color='crimson')
mongol_empire.plot(ax=ax2, 
                   transform=ccrs.PlateCarree(), 
                   color='blue')
overlap.plot(ax=ax2, 
             transform=ccrs.PlateCarree(), 
             color='green')

ax2.axis('off')
plt.show()