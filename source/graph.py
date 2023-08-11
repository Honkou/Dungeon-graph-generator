"""File for graph ABC and its implementations."""

import random
from abc import ABC, abstractmethod
from collections.abc import Iterable

import networkx as nx


class Graph(ABC):

    """Class for creating and analyzing graphs."""

    @abstractmethod
    def generate_graph(self, points: Iterable[int]) -> None:
        """Based on the given points, create nodes with edges."""

    @abstractmethod
    def add_legal_edge(self, new_point: int) -> None:
        """Create a connection between a freshly created node and an old one."""

    @abstractmethod
    def find_proper_nodes(self, excluded: int) -> list:
        """Return all nodes that match certain conditions."""


class NxGraph(Graph):

    """Implementation of NetworkX library's graph."""

    def __init__(self) -> None:
        """Initialize the class and assign a graph object."""
        self.graph = nx.Graph()
        self._EDGE_TRESHOLD = 4

    def generate_graph(self, points: Iterable[int]) -> None:
        """Based on the points given, create nodes with edges."""
        for point in points:
            max_edge = random.randint(2, self._EDGE_TRESHOLD)
            self.graph.add_node(point, label=str(point), max_edges=max_edge)

            if self.graph.number_of_nodes() > 1:
                edge_loop = random.randint(1, max_edge)
                for _ in range(edge_loop):
                    self.add_legal_edge(point)

    def add_legal_edge(self, new_point: int) -> None:
        """Create a connection between a freshly created node and a random old one.

        The random old node is determined by its availability.
        If a node of id 0 is chosen, that means that there are no valid nodes
        and no edge should be created.
        """
        random_node = random.choice(self.find_proper_nodes(new_point))
        if random_node == 0:
            return
        self.graph.add_edge(new_point, random_node)

    def find_proper_nodes(self, excluded: int) -> list[int]:
        """Return all nodes that match certain conditions.

        The conditions are:
        - the node is not the excluded one (usually excluding itself in the loop),
        - the node can have more edges creared, based on the max_edges property.

        Returns a list containing only 0 if there are no nodes matching these conditions.
        """
        proper_nodes = []
        for node in self.graph.nodes:
            if (
                node == excluded
                or self.graph.degree[node] >= nx.get_node_attributes(self.graph, "max_edges")[node]
            ):
                continue
            proper_nodes.append(node)
        if proper_nodes == []:
            return [0]
        return proper_nodes
