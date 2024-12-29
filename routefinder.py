import osmnx as ox
import networkx as nx
import matplotlib.pyplot as plt
import traceback
import copy


ox.settings.use_cache = True
ox.settings.log_console = True

# Define the path to your GraphML file
graphml_path = "combined_cities.graphml"

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

def get_distance_input(prompt):
    while True:
        distance_str = input(prompt).strip()
        print(distance_str)
        try:
            distance = float(distance_str)
            if distance > 0:
                return distance
            else:
                print("cant be neg")


        except ValueError:
            print("must be a number")

def find_nodes_at_distance(G, source, distance, tolerance = 100):

    length = nx.single_source_dijkstra_path_length(G, source, cutoff= distance + tolerance, weight = 'length')
    target_nodes = [node for node, dist in length.items() if distance - tolerance <= dist <= distance + tolerance]
    return target_nodes

def calculate_path_length(G, path):

    total_length = 0
    for u, v in zip(path[:-1], path[1:]):
        edge_data = G.get_edge_data(u, v)
        if edge_data:
            total_length += edge_data[0]['length']
    
    return total_length

def get_loop_choice(prompt):
    while True:
        choice = input(prompt).strip().lower()

        if choice in ['yes', 'y']:
            return True
        elif choice in ['no', 'n']:
            return False
        else:
            print('valid input please')
def find_best_loop(G, start_node, desired_distance, initial_tolerance = 100, max_tolerance = 100, step = 100):
    tolerance = initial_tolerance
    best_loop = None
    smallest_diff = float('inf')

    while tolerance <= max_tolerance:
        midpoint_nodes = find_nodes_at_distance(G, start_node, desired_distance /2 , tolerance)

        if not midpoint_nodes:
            tolerance += step
            continue
        
        for midpoint in midpoint_nodes:
            try:
                path_to_mid = nx.shortest_path(G, start_node, midpoint, weight = 'length')
                length_to_mid = calculate_path_length(G, path_to_mid)
                
            

                penalty_factor = 3
                orignal_lengths = {}

                for u, v in zip(path_to_mid[:-1], path_to_mid[1:]):
                    if G.has_edge(u ,v):
                        for key in G[u][v]:
                            orignal_lengths[(u, v, key)] = G[u][v][key]['length']
                            G[u][v][key]['length'] *= penalty_factor
                try:
                    path_back = nx.shortest_path(G, midpoint, start_node, weight = 'length')
                    length_back = calculate_path_length(G, path_back)

                    total_length = length_to_mid + length_back
                    diff  = abs(total_length - desired_distance_meter)

                    if diff < smallest_diff:
                        smallest_diff = diff
                        best_loop = path_to_mid + path_back[1:]
                except nx.NetworkXNoPath:
                    print("no path")
                for (u, v, key), orignal_length in orignal_lengths.items():
                    G[u][v][key]['length'] = orignal_length
            except Exception as e:
                print("Error finding midpoint")
                traceback.print_exc()
        if best_loop:
            return best_loop
        
        tolerance += step
    print("no good routes")
    return None

is_loop = get_loop_choice("do u  want a loop (yes ,no) ? : ")

if is_loop:


    start_address = get_address_input("start: ")

    desired_distanec_miles = get_distance_input("distance: ")

    miles_to_meter = 1609.34

    desired_distance_meter = desired_distanec_miles * miles_to_meter

    try:
        start_location = ox.geocode(start_address)
    except Exception as e:
        print("invalid start")
    try:
        start_node = ox.nearest_nodes(G, start_location[1], start_location[0])
    except Exception as e:
        print("invalid start")

    best_loop = find_best_loop(G, start_node, desired_distance_meter)

    if best_loop:
        loop_route = best_loop
    else:
        loop_route = None
        print("no route")

else:
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
if is_loop and loop_route:
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
            loop_route, 
            node_size=0, 
            edge_color='blue', 
            edge_linewidth=2, 
            ax=ax, 
            show=True, 
            close=True
        )
    except ImportError as e:
        print("error drawing")
# (Optional) Visualize the Route
elif not is_loop and route:
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
