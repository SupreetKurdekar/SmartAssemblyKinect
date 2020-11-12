import itertools
import networkx as nx
import matplotlib.pyplot as plt
import graph_utils as gUtils
import pygraphviz as pgv
from networkx.drawing.nx_agraph import graphviz_layout

# feasible fit graph
# for ABCDE chain link system
ff_graph = nx.Graph()
ff_graph.add_edges_from([("A","B"),("B","C"),("C","D"),("D","E"),("A","E")])
# ff_graph.add_edges_from([("L","B"),("L","S"),("R","B"),("R","S")])

nx.draw(ff_graph, with_labels=True, arrows=False)
plt.show()