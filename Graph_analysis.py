
def make_complete_graph(num_nodes):
    """
    Makes up a dictionary representing a directed graph with all possible edges. No loop links
    """
    node_list = []
    dictionary = {}
    # create list of nodes
    node_list = [node for node in range(0, num_nodes)]        
    for node in node_list:
        dictionary[node] = set()
        for node1 in node_list:
            if (node1 != node):
                dictionary[node].add(node1)
    return dictionary

def compute_in_degrees(digraph):
    """
    Computing in-degree of a directed graph inputed as a dictionary
    """
    in_degrees = {}
    for key in digraph.keys():
        in_degrees[key] = 0
    for values in digraph.values():
        for value in values:
            in_degrees[value] += 1
    return in_degrees

def in_degree_distribution(digraph):
    """
    Computes distribution of degrees in directed graph inputed as a dict
    """
    in_deg_distr = {}
    in_degrees = compute_in_degrees(digraph)
    for value in in_degrees.values():
        in_deg_distr[value] = 0
    for value in in_degrees.values():
        in_deg_distr[value] += 1
    return in_deg_distr
