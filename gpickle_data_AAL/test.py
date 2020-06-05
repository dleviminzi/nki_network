import networkx as nx
import numpy as np
import os
import pickle
from matplotlib import pyplot as plt
from sklearn.metrics import r2_score


f = open('sub-0021001_ses-1_dwi_AAL.gpickle', 'r')
G = nx.Graph(pickle.load(f))

print(G)
print(G.nodes())

density = nx.density(G)
avg_clustering = nx.average_clustering(G, weight='weight')
    #print('smlwrld: {}\n'.format(nx.sigma(G)))

    # graphing topological hierarchy (Negative correlation btwn degree
    # and clustering coefficient)
clst_nodes = nx.clustering(G, weight='weight')
deg_nodes = G.degree(weight='weight')

cn_values = []
for value in clst_nodes.values():
    cn_values.append(value)

#dg_values = []
#for i in range(len(deg_nodes)):
#    dg_values.append(deg_nodes[i+1])

print(deg_nodes)
