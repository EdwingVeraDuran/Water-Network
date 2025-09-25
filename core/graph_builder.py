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
            self.graph.add_edge(edge.n1, edge.n2)
        return self.graph
