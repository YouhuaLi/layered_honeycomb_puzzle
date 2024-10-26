from sage.all import *


# Check if the correct number of arguments are provided
if len(sys.argv) != 3:
    print("Usage: python lad_generate.py <layer> <d>")
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
            if abs( i - j ) >= d and abs( i - j ) <= 33:
                graph.add_edge(i, j)

    # Print the graph
    # print(graph)
    p = graph.plot()
    #p.save('big_graph.png')
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

#generate a gfu file for grahp g
def generate_gfu_file(g, filename, graph_name="test_graph"):
    with open(filename, 'w') as f:
        f.write('%d\n' % g.order())
        for v in g.vertices():
            f.write('%d\n' % v.degree())
            f.write('%d\n' % v.edges() )

def export_graph_to_lad(graph, filename):
    # 获取图的顶点数量
    n = graph.num_verts()
    
    # 打开文件准备写入
    with open(filename, 'w') as file:
        # 写入第一行，顶点的数量
        file.write(f"{n}\n")
        
        # 写入每个顶点的邻居信息
        for vertex in graph.vertices():
            # 获取当前顶点的继承节点（邻接顶点）
            successors = graph.neighbors(vertex)
            # 每个邻接顶点的标签减1
            neighbors_minus_one = [neighbor - 1 for neighbor in successors]
            # 写入当前顶点的继承节点数量及其继承节点
            file.write(f"{len(successors)} {' '.join(map(str, neighbors_minus_one))}\n")


#pattern_graph = generate_hexagonal_grid_graph(layer)

candidate_graph = generate_candidate_graph(layer, d)

#export_graph_to_lad(pattern_graph, f'/Users/youhua.li/code/math/layered_honeycomb_puzzle/layer/{layer}/pattern.lad')

export_graph_to_lad(candidate_graph, f'/Users/youhua.li/code/math/layered_honeycomb_puzzle/layer/{layer}/distance-{d}.lad')
