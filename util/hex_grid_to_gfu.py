import itertools
import math
import networkx as nx

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

def hex_grid_to_gfu(grid):
    """
    Converts the hex grid to GFU format.
    """
    lad_data = list(grid)
    edges = set()
    for hex in lad_data:
        neighbors = [n for n in hex_neighbors(hex) if n in grid]
        for neighbor in neighbors:
            edge = tuple(sorted((lad_data.index(hex), lad_data.index(neighbor))))
            edges.add(edge)
    
    gfu_data = "#hexagon_grid\n"
    gfu_data += f"{len(lad_data)}\n"
    gfu_data += ("a\n" * len(lad_data))
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

def main(rings, output_file):
    rings = rings - 1
    grid = generate_hex_grid(rings)
    gfu_data = hex_grid_to_gfu(grid)
    save_gfu_file(gfu_data, output_file)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Convert hex grid to GFU format.")
    parser.add_argument("rings", type=int, help="Number of rings around the central hexagon.")
    parser.add_argument("output_file", type=str, help="Path to the output GFU file.")
    args = parser.parse_args()
    main(args.rings, args.output_file)
