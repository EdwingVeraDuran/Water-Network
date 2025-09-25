import ezdxf
from models.node import Node
from models.edge import Edge
from models.node_type import NodeType

BLOCK_MAP: dict[str, NodeType] = {
    "APARATO": NodeType.APARATO,
    "VALVULA": NodeType.VALVULA,
    "ACOMETIDA": NodeType.ACOMETIDA,
    "ACCESORIO": NodeType.ACCESORIO,
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
        
        val_id = 1
        apa_id = 1
        acc_id = 1
        
        for insert in self.msp.query("INSERT"):
            x, y = insert.dxf.insert.x, insert.dxf.insert.y
            block_name = insert.dxf.name.upper()
            
            node_type = BLOCK_MAP.get(block_name)
            
            if (node_type == NodeType.VALVULA):
                node: Node = Node(id=f"V{val_id}", pos=(x, y), node_type=node_type)
                val_id += 1
            elif (node_type == NodeType.APARATO):
                node: Node = Node(id=f"AP{apa_id}", pos=(x, y), node_type=node_type)    
                apa_id += 1
            elif (node_type == NodeType.ACCESORIO):
                node: Node = Node(id=f"AC{acc_id}", pos=(x, y), node_type=node_type)
                acc_id += 1
            else:
                node: Node = Node(id=f"N{node_id}", pos=(x, y), node_type=node_type,)
                node_id += 1
        
            self.nodes.append(node)
            
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
            