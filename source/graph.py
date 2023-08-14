"""File for graph ABC and its implementations."""

import random
from abc import ABC, abstractmethod
from collections.abc import Iterable

import networkx as nx


class NodeNotFoundError(Exception):

    """Exception to be raised when there are no valid nodes to return."""


class Graph(ABC):

    """Class for creating and analyzing graphs."""

    @abstractmethod
    def __init__(self, max_edges: int) -> None:
        """Initialize the class and assign a graph object."""

    @abstractmethod
    def generate_graph(self, points: Iterable[int]) -> None:
        """Based on the given points, create nodes with edges."""

    @abstractmethod
    def _add_legal_edge(self, new_point: int) -> None:
        """Create a connection between a freshly created node and an old one."""

    @abstractmethod
    def _find_proper_nodes(self, excluded: int) -> list:
        """Return all nodes that match certain conditions."""

    @abstractmethod
    def _add_missing_edges(self) -> None:
        """Add missing edges for nodes with fewer edges than max_edges."""


class NxGraph(Graph):

    """Implementation of NetworkX library's graph."""

    def __init__(self, max_edges: int = 4) -> None:
        """Initialize the class and assign a graph object."""
        self.graph = nx.Graph()
        self._EDGE_TRESHOLD = max_edges

    def generate_graph(self, points: Iterable[int]) -> None:
        """Based on the points given, create nodes with edges."""
        for point in points:
            max_edge = random.randint(2, self._EDGE_TRESHOLD)
            self.graph.add_node(point, label=str(point), max_edges=max_edge)

            if self.graph.number_of_nodes() > 1:
                edge_loop = random.randint(1, max_edge - 1)
                for _ in range(edge_loop):
                    self._add_legal_edge(point)

        self._add_missing_edges()

    def _add_legal_edge(self, new_point: int) -> None:
        """Create a connection between a freshly created node and a random old one.

        The random old node is determined by its availability.
        If there are no valid nodes, then no edge should be created.
        """
        try:
            random_node = random.choice(self._find_proper_nodes(new_point))
        except NodeNotFoundError:
            return
        self.graph.add_edge(new_point, random_node)

    def _find_proper_nodes(self, excluded: int | None = None) -> list[int]:
        """Return all nodes that match certain conditions.

        The conditions are:
        - the node is not the excluded one (usually excluding itself in the loop),
        - the node can have more edges created, based on the max_edges property.

        Raise an exception if there are no nodes matching these conditions.
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
            raise NodeNotFoundError
        return proper_nodes

    def _add_missing_edges(self) -> None:
        """Add missing edges for nodes with fewer edges than max_edges."""
        for node in self.graph.nodes:
            max_edges = nx.get_node_attributes(self.graph, "max_edges")[node]
            current_degree = self.graph.degree[node]
            missing_edges = max_edges - current_degree

            if missing_edges > 0:
                try:
                    free_nodes = self._find_proper_nodes(node)
                except NodeNotFoundError:
                    continue

                num_edges_to_add = min(missing_edges, len(free_nodes))
                nodes_to_connect = random.sample(free_nodes, num_edges_to_add)

                for new_neighbor in nodes_to_connect:
                    self.graph.add_edge(node, new_neighbor)
