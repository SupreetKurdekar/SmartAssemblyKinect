import itertools
import networkx as nx
import matplotlib.pyplot as plt
import graph_utils as gUtils
import pygraphviz as pgv
from networkx.drawing.nx_agraph import graphviz_layout

# all ordering, storing and naming will be in lexicographic order

parts = ["A","B","C","D","E"]

# feasible fit graph
# for ABCDE chain link system
ff_graph = nx.Graph()
ff_graph.add_edges_from([("A","B"),("B","C"),("C","D"),("D","E"),("A","E")])
# nx.draw(ff_graph, with_labels=True, arrows=False)

# parts = parts.sorted()
# print(parts)

hierarchy = {}
for r in range(1,len(parts)+1):
	inner_list = list(itertools.combinations(parts, r))
	hierarchy[r] = inner_list

max_level = len(hierarchy)

G = nx.Graph()

for level in reversed(list(hierarchy.keys())):
	for node in hierarchy[level]:
		# node = set(node)
		nodeName = ""
		for s in node:
			nodeName += s
		# print(type(nodeName))
		G.add_node(nodeName,parts = node,level = level)

# make a new graph
G2 = nx.Graph()

# convert all nodes to nodes with sets. 
for node in G.nodes(data=True):
    G2.add_node(node[0],parts = set(node[1]["parts"]),level = node[1]["level"])

for level_num in range(1,max_level):
    # iterating through one level nodes in G2
    for node_name,node_data in G2.nodes(data=True):
        if node_data['level']==level_num:
            #iterating through all nodes above current level
            for upper_node_name,upper_node_data in G2.nodes(data=True):
                if upper_node_data['level'] > level_num:
                    # making edges if lower is subset of upper node
                    if node_data["parts"].issubset(upper_node_data["parts"]):
                        G2.add_edge(node_name,upper_node_name)

# remove the geometrically infeasible nodes
to_be_removed = []
for node in G2.nodes(data=True):
    if not gUtils.infeasible_reject(node,ff_graph):
        to_be_removed.append(node[0])
G2.remove_nodes_from(to_be_removed)

# # go through each edge of each node and remove each edge that does not have a complement
# # if complement is found store complement edge as anding edges

# for node_name,node_data in G2.nodes(data=True):
#     for neighbour in G2.neighbors(node_name):
        
#         comp = node_data["parts"].difference(G2.nodes[neighbour]["parts"])

#         print(comp)

# for level_num in range(1,max_level):



# # for level_num in range(1,max_level):
# #     # iterating through one level nodes in G2
# #     for node_name,node_data in G2.nodes(data=True):
# #         if node_data['level']==level_num:
# #             #iterating through all nodes above current level
# #             for upper_node_name,upper_node_data in G2.nodes(data=True):
# #                 if upper_node_data['level'] > level_num:
# #                     # making edges if lower is subset of upper node
# #                     if node_data["parts"].issubset(upper_node_data["parts"]):
# #                         diff_set = upper_node_data["parts"].difference(node_data["parts"])
                        

# write dot file to use with graphviz
# run "dot -Tpng test.dot >test.png"
nx.nx_agraph.write_dot(G2,'test.dot')

# same layout using matplotlib with no labels
pos=graphviz_layout(G2, prog='dot')
nx.draw(G2, pos, with_labels=True, arrows=False,node_size=1000)
plt.show()