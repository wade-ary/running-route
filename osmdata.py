import osmnx as ox
import matplotlib.pyplot as plt

# Configure OSMnx settings
ox.settings.use_cache = True
ox.settings.log_console = True

# Define the cities
cities = [
    "Boston, Massachusetts, USA",
    "Cambridge, Massachusetts, USA",
    "Allston, Massachusetts, USA",
    "Brookline, Massachusetts, USA",
    "Somerville Massachusetts, USA"


  

   
]

# Create a combined polygon for all cities
try:
    combined_polygon = ox.geocode_to_gdf(cities).unary_union
    print("Successfully created combined polygon for all cities.")
except Exception as e:
    print(f"Error creating combined polygon: {e}")
    exit(1)

# Step 1: Download the full graph
try:
    G = ox.graph_from_polygon(combined_polygon, network_type='all', simplify=True)
    print(f"Downloaded graph with {G.number_of_nodes()} nodes and {G.number_of_edges()} edges.")
except Exception as e:
    print(f"Error downloading graph: {e}")
    exit(1)

# Step 2: Filter the graph to remove unnecessary road types
def filter_graph(G):
    # Define highway types to remove
    remove_highways = {
        'motorway', 'trunk', 'motorway_link', 'trunk_link',  # Highways
        'service', 'unclassified', 'road'                   # Other less relevant road types
    }
    
    # Collect edges to remove
    edges_to_remove = []
    for u, v, k, d in G.edges(keys=True, data=True):
        if 'highway' in d:
            highway_type = d['highway']
            # Check if the highway type is in the removal set
            if isinstance(highway_type, list):
                if any(ht in remove_highways for ht in highway_type):
                    edges_to_remove.append((u, v, k))
            else:
                if highway_type in remove_highways:
                    edges_to_remove.append((u, v, k))

    # Remove the edges
    G.remove_edges_from(edges_to_remove)
    
    # Manually remove isolated nodes
    G = remove_isolated_nodes(G)
    
    return G

# Helper function to remove isolated nodes
def remove_isolated_nodes(graph):
    isolated_nodes = [node for node in graph.nodes if graph.degree(node) == 0]
    graph.remove_nodes_from(isolated_nodes)
    return graph

try:
    G = filter_graph(G)
    print(f"Filtered graph with {G.number_of_nodes()} nodes and {G.number_of_edges()} edges.")
except Exception as e:
    print(f"Error during filtering: {e}")
    exit(1)

# Step 3: Save the filtered graph
output_file = "filtered_combined_cities_wits.graphml"
ox.save_graphml(G, filepath=output_file)
print(f"Filtered graph saved to {output_file}")

# Step 4: Plot the graph
try:
    ox.plot_graph(G, node_size=0, edge_color='blue', edge_linewidth=0.5)
except Exception as e:
    print(f"Error during visualization: {e}")








