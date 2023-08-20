"""Test suite for the graph module."""
import copy
from pathlib import Path

import networkx as nx

from source.graph import NxGraph


def test_write_read(tmp_path: Path):
    """Assert that writing and reading the graph to a file doesn't change its inner structure."""
    file_name = tmp_path / "test.JSON"
    test_graph = NxGraph()
    test_graph.generate_graph(range(1, 11))
    original_graph = copy.deepcopy(test_graph.graph)
    test_graph.save_to_file(file_name)
    test_graph.read_from_file(file_name)
    assert nx.utils.graphs_equal(original_graph, test_graph.graph)
