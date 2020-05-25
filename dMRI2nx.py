import networkx as nx

def dMRI2nx(gpickle_path):
    unpickled = nx.read_gpickle(gpickle_path)
    G = nx.Graph()
    print(type(unpickled))
    for key in unpickled.edge.keys():
        weighted = unpickled.edge[key]
        for target in weighted.keys():
            weight = weighted.get(target).get('weight')
            G.add_edge(key, target, weight=weight)

    return G
