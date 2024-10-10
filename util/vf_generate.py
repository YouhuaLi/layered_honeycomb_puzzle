from sage.all import *
#from sage.graphs.generic_graph_pyx import SubgraphSearch
# layer number of the problem
layer =  4

# target distance
d = 9

# Generate the candidate big graph
def generate_candidate_graph(layer, d):
    # Define the numbers
    numbers = list(range(1, 3*layer*(layer-1) + 2))

    # Initialize the graph
    graph = Graph()

    # Add the vertices to the graph
    graph.add_vertices(numbers)

    # Add edges based on the absolute difference condition
    for i in numbers:
        for j in range(i+1, len(numbers)+1):
            if abs( i - j ) >= d:
                graph.add_edge(i, j)

    # Print the graph
    # print(graph)
    p = graph.plot()
    p.save('big_graph.png')
    return graph


def generate_hexagonal_grid_graph(n):
    """
    生成n圈的六边形网格图，每个六边形作为一个节点，相邻六边形作为边。
    
    参数：
    n -- 六边形的圈数
    
    返回：
    G -- 生成的六边形网格图
    """
    G = Graph()

    # 计算总的六边形数量
    total_hexagons = 1 + 3 * n * (n - 1)  # 总和公式

    # 添加节点
    G.add_vertices(range(1, total_hexagons + 1))

    # 添加边
    def add_edge_if_valid(a, b):
        if 1 <= a <= total_hexagons and 1 <= b <= total_hexagons:
            G.add_edge(a, b)

    # 邻接关系生成规则
    current_hexagon = 1  # 从中心的六边形开始, 中心的ring号为0
    last_inner_ring_begin_hex = 1 # 上一圈的起始编号
    if n >= 1:
        for ring in range(1, n):
            start_hex = current_hexagon + 1  # 当前圈的起始编号
            hexagons_in_ring = 6 * ring  # 当前圈中的六边形数量
            for i in range(hexagons_in_ring):
                hex_id = start_hex + i
                # 每个六边形与下一个六边形相邻（当前圈的边）
                add_edge_if_valid(hex_id, hex_id + 1 if i != hexagons_in_ring - 1 else start_hex)
                #每一圈的最小号码与内圈最小号码相邻。此后每隔圈数号，相邻一次，否则相邻2次
                if (hex_id - start_hex) % ring == 0:
                    add_edge_if_valid(hex_id, last_inner_ring_begin_hex + i // ring if ring != 1 else 1)
                else:
                    add_edge_if_valid(hex_id, last_inner_ring_begin_hex + i // ring)
                    add_edge_if_valid(hex_id, last_inner_ring_begin_hex + i // ring + 1  if i != hexagons_in_ring - 1 else last_inner_ring_begin_hex )
            current_hexagon = start_hex + hexagons_in_ring - 1  # 更新当前编号为当前圈的最后一个编号
            last_inner_ring_begin_hex = start_hex # 更新上一圈的起始编号为当前圈的起始编号
    
    # 返回生成的图
    return G

def export_graph_to_vf(graph, filename):
    # Get the number of vertices in the graph
    n = graph.num_verts()
    
    # Open the file to write
    with open(filename, 'w') as file:
        # Write the number of nodes
        file.write(f"{n}\n\n")
        
        # Write node attributes (here using the node index as the attribute)
        #file.write("# Node attributes\n")
        for vertex in graph.vertices():
            # Assuming the node attribute is the node index, but you can modify as needed
            file.write(f"{vertex - 1 } 1\n")
        
        file.write("\n")
        
        # Write edges information
        for vertex in graph.vertices():
            # Get the outgoing edges for the vertex
            edges = graph.edges_incident(vertex)
            # Write the number of outgoing edges from this node
            #file.write(f"# Edges coming out of node {vertex - 1}\n")
            file.write(f"{len(edges)}\n")
            
            # Write each edge information
            for edge in edges:
                u, v, edge_attr = edge
                if u == vertex:
                    file.write(f"{u-1} {v-1}\n")
                else:
                    file.write(f"{v-1} {u-1}\n")
            file.write("\n")

pattern_graph = generate_hexagonal_grid_graph(layer)
export_graph_to_vf(pattern_graph, f'/Users/youhua.li/code/vf3lib/hexagon/pattern_{layer}.vf')


target_graph = generate_candidate_graph(layer, d)
export_graph_to_vf(target_graph, f'/Users/youhua.li/code/vf3lib/hexagon/target_{layer}_{d}.vf')

