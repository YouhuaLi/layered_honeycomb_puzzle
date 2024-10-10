from sage.all import *
import sys

# Check if the correct number of arguments are provided
if len(sys.argv) != 3:
    print("Usage: python gfu_generate.py <layer> <d>")
    sys.exit(1)

# Parse command line arguments
layer = int(sys.argv[1])
d = int(sys.argv[2])

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

def export_graph_to_gfu(graph, filename, graph_name="graph"):
    # 获取节点数
    num_vertices = graph.num_verts()

    # 打开文件写入
    with open(filename, 'w') as file:
        # 写入图名称
        file.write(f"#{graph_name}\n")
        
        # 写入节点数量
        file.write(f"{num_vertices}\n")
        
        # 写入节点标签，假设每个节点的标签为其索引（你可以自定义标签）
        for vertex in graph.vertices():
            file.write(f"a\n")
        
        # 获取边的数量
        num_edges = graph.num_edges()
        file.write(f"{num_edges}\n")
        
        # 写入边信息，每条边两个节点（无向图，每条边只写一次）
        for u, v in graph.edges(labels=False):
            file.write(f"{u-1} {v-1}\n")

pattern_graph = generate_hexagonal_grid_graph(layer)

target_graph = generate_candidate_graph(layer, d)

export_graph_to_gfu(pattern_graph, filename=f'/Users/youhua.li/code/math/layered_honeycomb_puzzle/layer/{layer}/pattern.gfu')

export_graph_to_gfu(target_graph, f'/Users/youhua.li/code/math/layered_honeycomb_puzzle/layer/{layer}/distance-{d}.gfu')
