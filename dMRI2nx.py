import networkx as nx
import math

def dMRI2nx(gpickle_path, threshold):
    unpickled = nx.read_gpickle(gpickle_path)
    G = nx.Graph()
    weights = []
    pot_edges = []
    print(type(G))

    for key in unpickled.edge.keys():
        weighted = unpickled.edge[key]
        for target in weighted.keys():
            weight = weighted.get(target).get('weight')
            weights.append(weight)
            pot_edges.append((key, target, weight))

    weights = sorted(weights)
    
    t = threshold/100

    for edge in pot_edges:
        if (edge[2] >= math.floor(t*len(weights))):
            G.add_edge(edge[0], edge[1])

    return G
