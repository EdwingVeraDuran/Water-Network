class Edge:
    def __init__(self, n1: str, n2: str):
        self.n1 = n1
        self.n2 = n2
        
    def __repr__(self):
        return f"<Edge {self.n1} - {self.n2}"