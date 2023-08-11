"""Main file to run the program."""
from graph import NxGraph
from pyvis.network import Network

test_points = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
G = NxGraph()
G.generate_graph(test_points)

visnet = Network()
visnet.from_nx(G.graph)
visnet.show("proof.html", notebook=False)
