from core.dxf_parser import DXFParser
from core.graph_builder import GraphBuilder
from core.visualizer import Visualizer

if __name__ == "__main__":
    parser = DXFParser("data/prueba.dxf")
    nodes = parser.parse_nodes()
    edges = parser.parse_edges()
    
    builder = GraphBuilder(nodes, edges)
    G = builder.build()
    
    farthest, dist = builder.farthest_node_weighted
    print(f"Nodo más lejano: {farthest}")
    print(f"Distancia nodo más lejano: {dist}")
    
    Visualizer.plot(G)