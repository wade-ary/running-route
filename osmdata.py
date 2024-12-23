import osmnx as ox

# Configure OSMnx settings individually
ox.settings.use_cache = True
ox.settings.log_console = True

# Define the area of interest
place_name = "Boston, Massachusetts, USA"

# Define a custom filter to include specific highway types
custom_filter = '["highway"~"footway|path|pedestrian|track"]'

# Download the graph using the custom filter
# By default, simplify=True, so the graph is already simplified
G = ox.graph_from_place(place_name, custom_filter=custom_filter, network_type='walk')

# Save the graph for future use
ox.save_graphml(G, filepath="boston_walkways.graphml")
print("Graph saved to boston_walkways.graphml")

# (Optional) Plot the walkways to visualize
try:
    ox.plot_graph(G, node_size=0, edge_color='blue', edge_linewidth=0.5)
except ImportError as e:
    print(f"Visualization Error: {e}")
except Exception as e:
    print(f"An unexpected error occurred during plotting: {e}")




