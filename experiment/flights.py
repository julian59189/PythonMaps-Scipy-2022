import pandas as pd
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from shapely.geometry import Point
import geopandas as gpd
from shapely.geometry import LineString

fig_w = 10
fig_h = 5

ports = pd.read_csv("resources/ports.csv")
airports = pd.read_csv("resources/airports", delimiter=',', 
                       names=['id', 'name', 'city', 'country', 'iata', 
                              'icao', 'lat', 'long', 'altitude', 'timezone',
                              'dst', 'tz', 'type', 'source'])

routes = pd.read_csv("resources/routes", 
                     delimiter=',', 
                     names=['airline', 'id', 'source_airport', 
                            'source_airport_id', 'destination_airport', 
                            'destination_airport_id', 'codeshare',
                            'stops', 'equitment'])


port_geometry = [Point(xy) for xy in zip(ports['lon'], ports['lat'])]
port_geodata = gpd.GeoDataFrame(ports, 
                                crs="EPSG:4326", 
                                geometry=port_geometry)

# plot ports
# fig, ax = plt.subplots(figsize=(fig_w,fig_h))
# port_geodata.plot(ax=ax)
# plt.show()

# warp to globe
# fig, ax = plt.subplots(subplot_kw={'projection': ccrs.Robinson()}, 
#                        figsize=(fig_w,fig_h))
# port_geodata.plot(ax=ax, transform=ccrs.PlateCarree())
# plt.show()

# list of colors: https://matplotlib.org/stable/gallery/color/named_colors.html
# fig, ax = plt.subplots(facecolor='black', 
#                        subplot_kw={'projection': ccrs.Robinson()}, 
#                        figsize=(fig_w,fig_h))
# ax.patch.set_facecolor('black')
# port_geodata.plot(ax=ax, transform=ccrs.PlateCarree(),
#              markersize=3, alpha=1, edgecolors='none', color='darkviolet')

# plt.setp(ax.spines.values(), color='black')
# plt.setp([ax.get_xticklines(), ax.get_yticklines()], color='black')
# ax.set_ylim(-7000000, 9000000)
# plt.show()


airport_geometry = [Point(xy) for xy in zip(airports['long'], 
                                            airports['lat'])]
airport_geodata = gpd.GeoDataFrame(airports, 
                                   crs="EPSG:4326", 
                                   geometry=airport_geometry)

# plit airports
# fig, ax = plt.subplots(facecolor='black', 
#                        subplot_kw={'projection': ccrs.Robinson()}, 
#                        figsize=(fig_w,5))
# ax.patch.set_facecolor('black')

# airport_geodata.plot(ax=ax, transform=ccrs.PlateCarree(), 
#                      markersize=4, alpha=1, color='crimson', 
#                      edgecolors='none')
# plt.setp(ax.spines.values(), color='black')
# plt.setp([ax.get_xticklines(), ax.get_yticklines()], color='black')
# ax.set_ylim(-7000000, 9000000)
# plt.show()

source_airports = airports[['name', 'iata', 'icao', 'lat', 'long']]
destination_airports = source_airports.copy()
source_airports.columns = [str(col) + '_source' for col in source_airports.columns]
destination_airports.columns = [str(col) + '_destination' for col in destination_airports.columns]

routes = routes[['source_airport', 'destination_airport']]
routes = pd.merge(routes, 
                  source_airports, 
                  left_on='source_airport', 
                  right_on='iata_source')
routes = pd.merge(routes, 
                  destination_airports, 
                  left_on='destination_airport', 
                  right_on='iata_destination')


routes_geometry = [LineString([[routes.iloc[i]['long_source'], 
                                routes.iloc[i]['lat_source']], 
                               [routes.iloc[i]['long_destination'], 
                                routes.iloc[i]['lat_destination']]]) 
                   for i in range(routes.shape[0])]

routes_geodata = gpd.GeoDataFrame(routes, 
                                  geometry=routes_geometry, 
                                  crs='EPSG:4326')

# fig, ax = plt.subplots(figsize=(fig_w,fig_h))
# ax.patch.set_facecolor('black')

# routes_geodata.plot(ax=ax, color='white', linewidth=0.1)

# plt.show()

fig, ax = plt.subplots(subplot_kw={'projection': ccrs.Robinson()}, 
                       figsize=(fig_w,fig_h))
ax.patch.set_facecolor('black')
routes_geodata.plot(ax=ax, 
                    transform=ccrs.Geodetic(), 
                    color='white', 
                    linewidth=0.1, 
                    alpha=0.1)
# plt.setp(ax.spines.values(), color='black')
# plt.setp([ax.get_xticklines(), ax.get_yticklines()], color='black')
# ax.set_ylim(-7000000, 8800000)
# plt.show()

airport_source_count = routes.source_airport.value_counts()
airport_destination_count = routes.destination_airport.value_counts()

print(airport_source_count)
airport_source_count = pd.DataFrame({'airport':airport_source_count.index, 
                                     'source_airport_count':airport_source_count.values})
airport_destination_count = pd.DataFrame({'airport':airport_destination_count.index, 
                                          'destination_airport_count':airport_destination_count.values})

airport_counts = pd.merge(airport_source_count, 
                          airport_destination_count, 
                          left_on="airport", 
                          right_on="airport")

airport_counts['count'] = airport_counts['source_airport_count'] + airport_counts['destination_airport_count'] 

airport_counts = pd.merge(airport_counts, 
                          airports, 
                          left_on="airport", 
                          right_on="iata")

geometry = [Point(xy) for xy in zip(airport_counts.long, 
                                    airport_counts.lat)]

airport_counts = gpd.GeoDataFrame(airport_counts, 
                                  geometry=geometry, 
                                  crs="EPSG:4326")

airport_counts['markersize'] = airport_counts['count'] / 10



fig, ax = plt.subplots(subplot_kw={'projection': ccrs.Robinson()}, 
                       figsize=(fig_w,fig_h))
ax.patch.set_facecolor('black')
routes_geodata.plot(ax=ax, 
                    transform=ccrs.Geodetic(), 
                    color='white', 
                    linewidth=0.1, 
                    alpha=0.1)
airport_counts.plot(ax=ax, 
                    transform=ccrs.PlateCarree(), 
                    markersize=airport_counts['markersize'], 
                    alpha=0.8, 
                    column=airport_counts['long'], 
                    cmap='jet', 
                    edgecolors='none')

plt.setp(ax.spines.values(), color='#090909')
plt.setp([ax.get_xticklines(), ax.get_yticklines()], color='#090909')
ax.set_ylim(-7000000, 8800000)
plt.show()