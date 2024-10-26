import networkx as nx
import matplotlib.pyplot as plt
import math

def hex_distance(a, b):
    """
    Calculates the distance between two hexagons in a cube coordinate system.
    """
    return max(abs(a[0] - b[0]), abs(a[1] - b[1]), abs(a[2] - b[2]))

def hex_neighbors(cube):
    """
    Returns the neighboring hexagons in a cube coordinate system.
    """
    directions = [
        (1, -1, 0), (-1, 1, 0),
        (1, 0, -1), (-1, 0, 1),
        (0, 1, -1), (0, -1, 1)
    ]
    neighbors = [(cube[0] + d[0], cube[1] + d[1], cube[2] + d[2]) for d in directions]
    return neighbors

def generate_hex_grid(rings):
    """
    Generates a hex grid using cube coordinates.
    The number of rings specifies how far the grid extends from the center.
    """
    grid = set()
    center = (0, 0, 0)
    for x in range(-rings, rings + 1):
        for y in range(max(-rings, -x - rings), min(rings, -x + rings) + 1):
            z = -x - y
            grid.add((x, y, z))
    return grid

def hex_grid_to_lad(grid):
    """
    Converts the hex grid to LAD format.
    """
    lad_data = list(grid)
    neighbors_data = {}
    for idx, hex in enumerate(lad_data):
        neighbors = [n for n in hex_neighbors(hex) if n in grid]
        neighbors_data[hex] = [lad_data.index(n) for n in neighbors]
    return lad_data, neighbors_data

def print_lad_data(lad_data, neighbors_data):
    """
    Prints the LAD data in the correct LAD format.
    """
    n = len(lad_data)
    print(n)
    for hex in lad_data:
        neighbors = neighbors_data[hex]
        neighbors_str = " ".join(map(str, neighbors))
        print(f"{len(neighbors)} {neighbors_str}")

def mapping_node_to_label(mappings):
    """
    Maps the node number to a label for visualization.
    """
    result = {}
    mappings = mappings[1:-1]
    mappings = mappings.split(") (")
    for map in mappings:
        map = map.split(" -> ")
        result[map[0]] = map[1]
    print (result)
    return result

def visualize_lad_to_png(lad_data, neighbors_data, output_file, mappings):
    """
    Visualizes the LAD data and saves it as a PNG file, with node numbers as labels, in a hexagonal layout.
    """
    G = nx.Graph()
    
    # Add nodes
    for idx, hex in enumerate(lad_data):
        G.add_node(idx)
    
    # Add edges
    for hex, neighbors in neighbors_data.items():
        for neighbor in neighbors:
            G.add_edge(lad_data.index(hex), neighbor)
    
    # Generate hexagonal layout for visualization
    pos = {}
    for idx, (q, r, s) in enumerate(lad_data):
        x = q + 0.5 * r
        y = r * math.sqrt(3) / 2
        pos[idx] = (x, y)
    
    # Draw the graph
    nx.draw(G, pos, with_labels=True, labels={node: mappings[str(node)] for node in G.nodes()},
            node_size=500, font_size=10, node_color='skyblue', edge_color='gray', font_weight='bold')
    plt.gca().set_aspect('equal')
    plt.savefig(output_file, bbox_inches='tight')
    plt.close()

def main(rings, image_file):
    rings = rings - 1 # Convert to 0-indexed
    grid = generate_hex_grid(rings)
    lad_data, neighbors_data = hex_grid_to_lad(grid)
    print_lad_data(lad_data, neighbors_data)

    mappings = "(0 -> 21) (1 -> 28) (2 -> 13) (3 -> 1) (4 -> 60) (5 -> 56) (6 -> 5) (7 -> 20) (8 -> 6) (9 -> 51) (10 -> 8) (11 -> 42) (12 -> 48) (13 -> 55) (14 -> 22) (15 -> 47) (16 -> 37) (17 -> 40) (18 -> 35) (19 -> 16) (20 -> 0) (21 -> 4) (22 -> 38) (23 -> 15) (24 -> 9) (25 -> 10) (26 -> 23) (27 -> 45) (28 -> 46) (29 -> 12) (30 -> 33) (31 -> 3) (32 -> 27) (33 -> 26) (34 -> 7) (35 -> 11) (36 -> 41) (37 -> 57) (38 -> 25) (39 -> 54) (40 -> 59) (41 -> 34) (42 -> 32) (43 -> 14) (44 -> 52) (45 -> 36) (46 -> 31) (47 -> 19) (48 -> 18) (49 -> 50) (50 -> 43) (51 -> 24) (52 -> 49) (53 -> 58) (54 -> 39) (55 -> 30) (56 -> 17) (57 -> 53) (58 -> 44) (59 -> 29) (60 -> 2)"
    mappings = mapping_node_to_label(mappings)
    visualize_lad_to_png(lad_data, neighbors_data, image_file, mappings)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Convert hex grid to LAD format and visualize it.")
    parser.add_argument("rings", type=int, help="Number of rings around the central hexagon.")
    parser.add_argument("image_file", type=str, help="Path to the output PNG file.")
    args = parser.parse_args()
    main(args.rings, args.image_file)
