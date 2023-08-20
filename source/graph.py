"""File for graph ABC and its implementations."""

import json
import random
from abc import ABC, abstractmethod
from collections.abc import Iterable
from pathlib import Path

import networkx as nx
from randomize_option import Function, randomize_function


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
    def save_to_file(self, path: Path) -> None:
        """Save the generated graph to a local file."""

    @abstractmethod
    def read_from_file(self, path: Path) -> None:
        """Read the saved file to a graph object."""

    @abstractmethod
    def _add_legal_edge(self, new_point: int) -> None:
        """Create a connection between a freshly created node and an old one."""

    @abstractmethod
    def _find_proper_nodes(self, current_node: int) -> list:
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
            likely_func = Function(self._generate_unique_edge_treshold, (point,))
            unlikely_func = Function(self._generate_random_edge_treshold)
            max_edge = randomize_function(
                likely_func,
                unlikely_func,
                chance=5,
            )

            self.graph.add_node(point, label=str(point), max_edges=max_edge)

            if self.graph.number_of_nodes() > 1:
                self._add_close_connections(node=point, edge_treshold=max_edge)

        self._add_missing_edges()
        print(nx.get_node_attributes(self.graph, "max_edges"))

    def save_to_file(self, path: Path) -> None:
        """Save the generated graph to a local file."""
        data = nx.readwrite.json_graph.node_link_data(self.graph)
        serialized_data = json.dumps(data)
        with Path(path).open("w") as file:
            file.write(serialized_data)

    def read_from_file(self, path: Path) -> None:
        """Read the saved file to a graph object."""
        with Path(path).open("r") as file:
            serialized_data = file.read()
        data = json.loads(serialized_data)
        self.graph = nx.readwrite.json_graph.node_link_graph(data)

    def _add_close_connections(self, node: int, edge_treshold: int) -> None:
        """Add edges from a node to somewhat closely neighbored nodes.

        This takes for account:
        - adding random ammount of connections to already generated nodes
        - leaving at least one additional empty space for future connections
        """
        max_amount_of_loops = max(edge_treshold - 1, 1)
        edge_loop = random.randint(1, max_amount_of_loops)
        for _ in range(edge_loop):
            self._add_legal_edge(node)

    def _generate_unique_edge_treshold(self, current_node: int) -> int:
        """For a node, generate max number of connections different from the previous node."""
        max_edge = random.randint(2, self._EDGE_TRESHOLD)
        if current_node == 1:
            return max_edge
        previous_node = current_node - 1
        previous_nodes_max = nx.get_node_attributes(self.graph, "max_edges")[previous_node]
        while previous_nodes_max == max_edge:
            max_edge = random.randint(2, self._EDGE_TRESHOLD)
        return max_edge

    def _generate_random_edge_treshold(self) -> int:
        """For a node, generate max number of connections."""
        return random.randint(2, self._EDGE_TRESHOLD)

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

    def _find_proper_nodes(self, current_node: int | None = None) -> list[int]:
        """Return all nodes that match certain conditions.

        The conditions are:
        - the node is not the current node,,
        - the node doesn't already have a connection with the current node,
        - the node can have more edges created with it, based on the max_edges property.

        Raise an exception if there are no nodes matching these conditions.
        """
        proper_nodes = []
        for node in self.graph.nodes:
            if (
                node == current_node
                or self.graph.has_edge(node, current_node)
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
