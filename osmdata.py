import osmnx as ox

# Define the area of interest
place = "Boston, Massachusetts, USA"

# Define the network type to include walkways
G = ox.graph_from_place(place, network_type='walk', simplify=True)

# Save the graph for later use
ox.save_graphml(G, "boston_walkways.graphml")
