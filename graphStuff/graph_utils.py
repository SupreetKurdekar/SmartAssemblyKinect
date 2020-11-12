import networkx as nx
import matplotlib.pyplot as plt

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
