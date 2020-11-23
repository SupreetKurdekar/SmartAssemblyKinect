import itertools
import networkx as nx
import matplotlib.pyplot as plt
import pygraphviz as pgv
from networkx.drawing.nx_agraph import graphviz_layout

def get_node_attribute_dictionary(graph,attribute):
    """This function takes a networkx graph as an input and returns a dictionary
    with node as key and requested attribute as value
    
    Args:
        graph (nx graph): input graph
        attribute ([string]): that data stored in node of the graph

    Returns:
        dictionary: keys are nodes of the graph and values are the required attributes
    """
    node_attribute_dict = {node_name: data[attribute] for node_name,data in graph.nodes(data=True)}

    return node_attribute_dict

def infeasible_reject(node,feasibility_graph):
    return nx.is_connected(feasibility_graph.subgraph(node[1]["parts"]))

def get_AO_graph(parts,feasible_edges):

    # feasible fit graph
    # for ABCDE chain link system
    ff_graph = nx.Graph()
    ff_graph.add_edges_from(feasible_edges)
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
    # add an attribute called anded_pairs
    # anded_pairs is a list of pairs of nodes which together form that node
    for node in G.nodes(data=True):
        G2.add_node(node[0],parts = set(node[1]["parts"]),level = node[1]["level"],anded_pairs = [])


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
                            # Each edge now has an trribute called anded which is currently set to False
                            G2[node_name][upper_node_name]['anded']=False


    # remove the geometrically infeasible nodes
    to_be_removed = []
    for node in G2.nodes(data=True):
        if not infeasible_reject(node,ff_graph):
            to_be_removed.append(node[0])
    G2.remove_nodes_from(to_be_removed)

    # # go through each edge of each node and remove each edge that does not have a complement
    # # if complement is found store complement edge as anding edges
    edges_to_be_removed = []

    for node_name,node_data in G2.nodes(data=True):
        for neighbour in G2.neighbors(node_name):
            if G2.nodes[neighbour]["level"] < node_data["level"]:
                anded_pair = []
                comp = node_data["parts"].difference(G2.nodes[neighbour]["parts"])
                comp_level = len(comp)
                for neighbour_2 in G2.neighbors(node_name):
                    if (neighbour_2 != neighbour) and (comp_level == G2.nodes[neighbour_2]["level"]) and (comp == G2.nodes[neighbour_2]["parts"]):
                        anded_pair.append(neighbour_2)
                        break
                if len(anded_pair)>0:
                    G2[node_name][neighbour]["anded"] = True
                    G2[node_name][anded_pair[0]]["anded"] = True
                    anded_pair.append(neighbour)
                    G2.nodes[node_name]['anded_pairs'].append(anded_pair)
                else:
                    edges_to_be_removed.append((node_name,neighbour))

    G2.remove_edges_from(edges_to_be_removed)

    # write dot file to use with graphviz
    # run "dot -Tpng test.dot >test.png"
    nx.nx_agraph.write_dot(G2,'test.dot')

    # same layout using matplotlib with no labels
    pos=graphviz_layout(G2, prog='dot')
    nx.draw(G2, pos, with_labels=True, arrows=False,node_size=1000)

    plt.savefig("Graph.png", format="PNG")
    plt.show()  
