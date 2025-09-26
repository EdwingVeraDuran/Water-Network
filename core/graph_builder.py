import networkx as nx

from models.edge import Edge
from models.node import Node

class GraphBuilder:
    def __init__(self, nodes: list[Node], edges: list[Edge]):
        self.nodes = nodes
        self.edges = edges
        self.graph = nx.Graph()
        
    def build(self):
        for node in self.nodes:
            self.graph.add_node(node.id, pos=node.pos, type=node.type, color=node.color)
        for edge in self.edges:
            self.graph.add_edge(edge.n1.id, edge.n2.id, weight=edge.length)
        return self.graph
    
    @property
    def farthest_node_weighted(self):
        # Search for initial node (Acometida)
        start_nodes = [n for n in self.nodes if n.type.name == "ACOMETIDA"]
        if not start_nodes:
            raise ValueError("No se encontro un nodo de tipo acometida en la red.")
        
        start_node = start_nodes[0].id
        
        # Get nodes distances from start_node
        lengths = nx.single_source_dijkstra_path_length(self.graph, start_node, weight="weight")
        
        # FIlter node type for "APARATO"
        apa_nodes = [n.id for n in self.nodes if n.type.name == "APARATO"]
        if not apa_nodes:
            raise ValueError("No se encontraron nodos de tipo aparato en la red.")
        
        
        
        farthest = max(apa_nodes, key=lambda n: lengths.get(n, float("-inf")))
        return farthest, lengths[farthest]
