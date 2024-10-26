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

def visualize_lad_file(neighbors_data, output_file):
    """
    Visualizes the LAD data and saves it as a PNG file.
    """
    G = nx.Graph()
    
    # Add nodes
    for node in neighbors_data.keys():
        G.add_node(node)
    
    # Add edges
    for node, neighbors in neighbors_data.items():
        for neighbor in neighbors:
            G.add_edge(node, neighbor)
    
    # Draw the graph using a planar layout
    #pos = nx.planar_layout(G)  # Use planar layout for visualization
    pos = nx.spring_layout(G)  # Use spring layout for visualization
    nx.draw(G, pos, with_labels=True, node_size=300, font_size=8, node_color='skyblue', edge_color='gray')
    plt.savefig(output_file)
    plt.close()

def main(input_file, output_file):
    neighbors_data = read_lad_file(input_file)
    visualize_lad_file(neighbors_data, output_file)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Visualize LAD format file and save as PNG.")
    parser.add_argument("input_file", type=str, help="Path to the input LAD format file.")
    parser.add_argument("output_file", type=str, help="Path to the output PNG file.")
    args = parser.parse_args()
    main(args.input_file, args.output_file)
