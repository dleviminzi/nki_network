import networkx as nx
import math

def dMRI2nx(gpickle_path, threshold, directed=False):
    unpickled = nx.read_gpickle(gpickle_path)
    weights = []
    pot_edges = []

    for key in unpickled.edge.keys():
        weighted = unpickled.edge[key]
        for target in weighted.keys():
            weight = weighted.get(target).get('weight')
            weights.append(weight)
            pot_edges.append((key, target, weight))

    weights = sorted(weights)
    if directed:
        G = nx.DiGraph()
    else:
        G = nx.Graph()
    print(type(G))
    t = threshold/100

    for edge in pot_edges:
        if (edge[2] >= weights[math.floor(t*len(weights))]):
            G.add_edge(edge[0], edge[1])
            if directed:
                G.add_edge(edge[1], edge[0])

    return G
