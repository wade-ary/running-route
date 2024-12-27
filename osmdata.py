import osmnx as ox
import matplotlib.pyplot as plt

# Configure OSMnx settings
ox.settings.use_cache = True
ox.settings.log_console = True

# Define the cities
cities = ["Boston, Massachusetts, USA", "Cambridge, Massachusetts, USA", "Brookline, Massachusetts, USA", "Allston, Massachusetts, USA"]

# Create a combined polygon for all cities
try:
    combined_polygon = ox.geocode_to_gdf(cities).unary_union
    print("Successfully created combined polygon for all cities.")
except Exception as e:
    print(f"Error creating combined polygon: {e}")
    exit(1)

# Download the graph for the combined polygon
try:
    G = ox.graph_from_polygon(combined_polygon, network_type='all', simplify=True)
    print(f"Downloaded graph with {G.number_of_nodes()} nodes and {G.number_of_edges()} edges.")
except Exception as e:
    print(f"Error downloading graph: {e}")
    exit(1)

# Save the graph
output_file = "combined_cities2.graphml"
ox.save_graphml(G, filepath=output_file)
print(f"Graph saved to {output_file}")

# Plot the graph
try:
    ox.plot_graph(G, node_size=0, edge_color='blue', edge_linewidth=0.5)
    
except Exception as e:
    print(f"Error during visualization: {e}")





