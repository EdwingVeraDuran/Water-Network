from models.node import Node
import math

class Edge:
    def __init__(self, n1: Node, n2: Node):
        self.n1 = n1
        self.n2 = n2
        
    @property
    def length(self):
        if hasattr(self.n1, "pos") and hasattr(self.n2, "pos"):
            x1, y1 = self.n1.pos
            x2, y2 = self.n2.pos
            return math.dist((x1, y1), (x2, y2))
        
    def __repr__(self):
        return f"<Edge {self.n1} - {self.n2}>"