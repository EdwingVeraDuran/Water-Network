import networkx as nx

from models.edge import Edge
from models.node import Node
from models.node_type import NodeType

class GraphBuilder:
    def __init__(self, nodes: list[Node], edges: list[Edge]):
        self.nodes = nodes
        self.edges = edges
        self.graph = nx.DiGraph()
        
    def build(self):
        # Add nodes
        for node in self.nodes:
            self.graph.add_node(node.id, pos=node.pos, type=node.type, color=node.color)
        
        # Step 1: Get "ACOMETIDA"
        acometidas = [n for n in self.nodes if n.type == NodeType.ACOMETIDA]
        if not acometidas:
            raise ValueError("No se encontró acometida en la red.")
        start_node = acometidas[0]
        
        # Step 2: BFS from ACOMETIDA
        visited = set([start_node.id])
        queue = [start_node]
        
        while queue:
            current = queue.pop(0)
            
            # Search for neighbors connected to edges
            neighbors = [e.n2 for e in self.edges if e.n1 == current] + [e.n1 for e in self.edges if e.n2 == current]
            
            for neighbor in neighbors:
                if neighbor.id not in visited:
                    length = Edge(current, neighbor).length
                    self.graph.add_edge(current.id, neighbor.id, weight=length)
                    
                    visited.add(neighbor.id)
                    queue.append(neighbor)
                    
        return self.graph
    
    @property
    def farthest_node_weighted(self):
        # Search for initial node (Acometida)
        start_nodes = [n for n in self.nodes if n.type == NodeType.ACOMETIDA]
        if not start_nodes:
            raise ValueError("No se encontro un nodo de tipo acometida en la red.")
        
        start_node = start_nodes[0].id
        
        # Get nodes distances from start_node
        lengths = nx.single_source_dijkstra_path_length(self.graph, start_node, weight="weight")
        
        # FIlter node type for "APARATO"
        apa_nodes = [n.id for n in self.nodes if n.type == NodeType.APARATO]
        if not apa_nodes:
            raise ValueError("No se encontraron nodos de tipo aparato en la red.")
        
        
        
        farthest = max(apa_nodes, key=lambda n: lengths.get(n, float("-inf")))
        return farthest, lengths[farthest]
