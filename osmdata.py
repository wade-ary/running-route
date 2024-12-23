import osmnx as ox
import matplotlib.pyplot as plt

# Optional: Configure OSMnx settings
ox.config(use_cache=True, log_console=True)

place_name = "Boston, Massachusetts, USA"

G_walk = ox.graph_from_place(place_name, network_type="walk")

# Define tags for parks and recreational areas
tags = {'leisure': ['park', 'garden', 'golf_course', 'playground', 'stadium']}

# Download polygons for parks in Boston
parks = ox.geometries_from_place(place_name, tags=tags)

# Optional: Save parks data to a file
parks.to_file("boston_parks.geojson", driver='GeoJSON')

trail_tags = {'highway': ['path', 'footway', 'cycleway']}

# Download trails and paths in Boston
trails = ox.geometries_from_place(place_name, tags=trail_tags)

# Optional: Save trails data to a file
trails.to_file("boston_trails.geojson", driver='GeoJSON')

fig, ax = ox.plot_graph(G_walk, show=False, close=False, node_size=0, edge_color='gray')

# Plot parks on the same map
parks.plot(ax=ax, facecolor='green', edgecolor='k', alpha=0.5)

# Optional: Plot trails
trails.plot(ax=ax, facecolor='blue', edgecolor='k', alpha=0.3)

plt.show()