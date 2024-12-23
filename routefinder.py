import osmnx as ox
import networkx as nx
import matplotlib.pyplot as plt

# Configure OSMnx settings
ox.settings.use_cache = True
ox.settings.log_console = True

# Define the path to your GraphML file
graphml_path = "boston_walkways.graphml"

# Load the graph from the GraphML file
G = ox.load_graphml(graphml_path)
print(f"Graph loaded with {G.number_of_nodes()} nodes and {G.number_of_edges()} edges.")

# Check if the graph is directed
print(f"Is the graph directed? {G.is_directed()}")

# Convert to undirected graph if necessary
if G.is_directed():
    print("Converting directed graph to undirected.")
    G = G.to_undirected()
else:
    print("Graph is already undirected.")

def get_address_input(prompt):
    while True:
        address = input(prompt).strip()
        if address:
            return address
        else:
            print("cannot be empty")
start_address = get_address_input("start: ")
end_address = get_address_input("end: ")
# Find the nearest nodes to the start and end points
try:
    start_location = ox.geocode(start_address)
    end_location = ox.geocode(end_address)
    print(f"Start Node: {start_location}")
    print(f"End Node: {end_location}")

except Exception as e:
    print(f"An unexpected error occurred while finding nearest nodes: {e}")
    exit(1)

try:
    start_node = ox.nearest_nodes(G, start_location[1], start_location[0])
    end_node = ox.nearest_nodes(G, end_location[1], end_location[0])
except Exception as e:
    print("error")
    exit(1)
# Compute the shortest path between start and end nodes
try:
    route = nx.shortest_path(G, start_node, end_node, weight='length')
    print("Route found successfully.")
    print(f"Route has {len(route)} nodes.")
    print(f"First 10 nodes in the route: {route[:10]}")
    print(f"Last 10 nodes in the route: {route[-10:]}")
    
    # Verify consecutive nodes are connected
    for i in range(len(route) - 1):
        if not G.has_edge(route[i], route[i+1]):
            print(f"Error: No edge between {route[i]} and {route[i+1]}")
            break
    else:
        print("All consecutive nodes in the route are connected.")
except nx.NetworkXNoPath:
    print("No path exists between the start and end points.")
    route = None
except Exception as e:
    print(f"An unexpected error occurred while finding the route: {e}")
    route = None

# (Optional) Visualize the Route
if route:
    try:
        # Plot the entire graph in light gray
        fig, ax = ox.plot_graph(
            G, 
            node_size=0, 
            edge_color='lightgray', 
            edge_linewidth=0.5, 
            bgcolor='white', 
            show=False, 
            close=False
        )
        
        # Plot the route in red on top of the gray graph
        ox.plot_graph_route(
            G, 
            route, 
            node_size=0, 
            edge_color='red', 
            edge_linewidth=2, 
            ax=ax, 
            show=True, 
            close=True
        )
    except ImportError as e:
        print(f"Visualization Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred during plotting: {e}")
