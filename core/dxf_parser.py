import ezdxf
from models.node import Node
from models.edge import Edge

BLOCK_MAP: map = {
    "APARATO": "aparato",
    "VALVULA": "valvula",
    "ACOMETIDA": "acometida",
    "ACCESORIO": "accesorio",
}

class DXFParser:
    def __init__(self, filepath: str):
        self.doc = ezdxf.readfile(filepath)
        self.msp = self.doc.modelspace()
        self.nodes: list[Node] = []
        self.edges: list[Edge] = []
        self.tol = 1e-3
        
    def parse_nodes(self):
        node_id = 1
        
        for insert in self.msp.query("INSERT"):
            x, y = insert.dxf.insert.x, insert.dxf.insert.y
            block_name = insert.dxf.name.upper()
            
            node_type = BLOCK_MAP.get(block_name)
            
            node: Node = Node(id=f"N{node_id}", pos=(x, y), node_type=node_type,)
            self.nodes.append(node)
            node_id += 1
        
        return self.nodes
    
    def find_node_by_coords(self, coord: tuple):
        for node in self.nodes:
            x, y = node.pos
            if abs(x - coord[0]) < self.tol and abs(y - coord[1]) < self.tol:
                return node
        return None
    
    def parse_edges(self):
        for line in self.msp.query("LINE"):
            start = (line.dxf.start.x, line.dxf.start.y)
            end = (line.dxf.end.x, line.dxf.end.y)
            
            n1 = self.find_node_by_coords(start)
            n2 = self.find_node_by_coords(end)
            
            if n1 and n2:
                edge: Edge = Edge(n1, n2)
                self.edges.append(edge)
                
        return self.edges
            