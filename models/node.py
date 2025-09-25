from models.node_type import NodeType

class Node:
    def __init__(self, id: str, pos: tuple, node_type: NodeType, color=None):
        self.id = id
        self.pos = pos
        self.type = node_type
        self.color = color
        
    def __repr__(self):
        return f"<Node {self.id} ({self.type}) at {self.pos}"