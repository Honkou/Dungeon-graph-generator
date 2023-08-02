import networkx as nx
from pyvis.network import Network

G = nx.Graph()
G.add_nodes_from([1,3,5,7,9])
G.add_edge(1,3)
G.add_edge(5,9)

print(G.number_of_edges())
print(G.number_of_nodes())

visnet = Network()
visnet.from_nx(G)
visnet.show("proof.html", notebook=False)