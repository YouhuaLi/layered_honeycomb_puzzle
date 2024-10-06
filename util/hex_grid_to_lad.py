import itertools
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

def print_lad_data_with_labels(lad_data, neighbors_data):
    """
    Prints the LAD data with index labels in the center of each hex grid.
    """
    n = len(lad_data)
    print(n)
    for idx, hex in enumerate(lad_data):
        neighbors = neighbors_data[hex]
        neighbors_str = " ".join(map(str, neighbors))
        print(f"{idx}: {len(neighbors)} {neighbors_str}")

def simulate_hex_grid_with_labels(rings):
    """
    Simulates the hex grid and prints LAD data with index labels.
    """
    grid = generate_hex_grid(rings)
    lad_data, neighbors_data = hex_grid_to_lad(grid)
    print_lad_data_with_labels(lad_data, neighbors_data)

def main(rings):
    rings = rings - 1 # Convert to 0-indexed
    grid = generate_hex_grid(rings)
    lad_data, neighbors_data = hex_grid_to_lad(grid)
    print_lad_data(lad_data, neighbors_data)
    #simulate_hex_grid_with_labels(rings)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Convert hex grid to LAD format.")
    parser.add_argument("rings", type=int, help="Number of rings around the central hexagon.")
    args = parser.parse_args()
    main(args.rings)
