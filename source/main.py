"""Main file to run the program."""
from graph import NxGraph
from pyvis.network import Network

test_points = range(1, 21)
G = NxGraph()
G.generate_graph(test_points)

physics_options = """const options = {
  "physics": {
    "barnesHut": {
      "gravitationalConstant": -1450,
      "centralGravity": 0.15,
      "springLength": 155,
      "springConstant": 0.015,
      "damping": 0.45
    },
    "minVelocity": 0.75
  }
}"""

visnet = Network()
visnet.from_nx(G.graph)
visnet.toggle_physics = True
visnet.set_options(physics_options)
visnet.show("proof.html", notebook=False)
