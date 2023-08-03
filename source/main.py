"""Main file to run the program."""
import random

import networkx as nx
from pyvis.network import Network


def generate_graph(points: tuple) -> nx.Graph:
    """Create a graph based on the points input."""
    graph = nx.Graph()
    for point in points:
        graph.add_node(point, label=str(point))
        if graph.number_of_nodes() > 1:
            random_node = random.choice(find_proper_nodes(graph, point))  # noqa: S311
            graph.add_edge(point, random_node)
    return graph


def find_proper_nodes(graph: nx.Graph, excluded: int) -> list:
    """Return all nodes that match certain conditions."""
    proper_nodes = []
    for node in graph.nodes:
        if node == excluded:
            continue
        proper_nodes.append(node)  # do: Add proper logic
    return proper_nodes


test_points = (1, 2, 3, 4, 5, 6)
G = generate_graph(test_points)

visnet = Network()
visnet.from_nx(G)
visnet.show("proof.html", notebook=False)
