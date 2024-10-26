import networkx as nx
import matplotlib.pyplot as plt

def read_lad_file(file_path):
    """
    Reads the LAD format file and returns the graph data.
    """
    with open(file_path, 'r') as f:
        lines = f.readlines()
        n = int(lines[0].strip())
        neighbors_data = {}
        for idx in range(1, n + 1):
            parts = lines[idx].strip().split()
            num_neighbors = int(parts[0])
            neighbors = list(map(int, parts[1:num_neighbors + 1]))
            neighbors_data[idx - 1] = neighbors
    return neighbors_data

def lad_to_gfu(neighbors_data):
    """
    Converts the LAD data to GFU format.
    """
    gfu_data = "#graph_from_lad\n"
    num_nodes = len(neighbors_data)
    gfu_data += f"{num_nodes}\n"
    gfu_data += ("a\n" * num_nodes)  # All nodes have label "a"
    
    edges = set()
    for node, neighbors in neighbors_data.items():
        for neighbor in neighbors:
            edge = tuple(sorted((node, neighbor)))
            edges.add(edge)
    
    gfu_data += f"{len(edges)}\n"
    for edge in edges:
        gfu_data += f"{edge[0]} {edge[1]}\n"
    
    return gfu_data

def save_gfu_file(gfu_data, output_file):
    """
    Saves the GFU data to a file.
    """
    with open(output_file, 'w') as f:
        f.write(gfu_data)

def visualize_grid_to_png(neighbors_data, output_file):
    """
    Visualizes the grid and saves it as a PNG file, with node numbers as labels.
    """
    G = nx.Graph()
    
    # Add nodes
    for node in neighbors_data.keys():
        G.add_node(node)
    
    # Add edges
    for node, neighbors in neighbors_data.items():
        for neighbor in neighbors:
            G.add_edge(node, neighbor)
    
    # Generate layout for visualization
    pos = nx.spring_layout(G)  # Use spring layout for visualization
    
    # Draw the graph
    nx.draw(G, pos, with_labels=True, labels={node: str(node) for node in G.nodes()},
            node_size=300, font_size=8, node_color='skyblue', edge_color='gray')
    plt.savefig(output_file)
    plt.close()

def main(input_file, output_file, image_file):
    neighbors_data = read_lad_file(input_file)
    gfu_data = lad_to_gfu(neighbors_data)
    save_gfu_file(gfu_data, output_file)
    visualize_grid_to_png(neighbors_data, image_file)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Convert LAD format file to GFU format and visualize the grid.")
    parser.add_argument("input_file", type=str, help="Path to the input LAD format file.")
    parser.add_argument("output_file", type=str, help="Path to the output GFU file.")
    parser.add_argument("image_file", type=str, help="Path to the output PNG file.")
    args = parser.parse_args()
    main(args.input_file, args.output_file, args.image_file)
