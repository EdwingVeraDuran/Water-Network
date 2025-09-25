import networkx as nx
import matplotlib.pyplot as plt

class Visualizer:
    @staticmethod
    def plot(graph: nx.Graph):
        pos = nx.get_node_attributes(graph, "pos")
        types = nx.get_node_attributes(graph, "type")
        
        nx.draw(graph, pos, with_labels=True)
        plt.show()