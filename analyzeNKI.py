from dMRI2nx import dMRI2nx
import networkx as nx
import numpy as np
from matplotlib import pyplot as plt
from sklearn.metrics import r2_score
import os

def analyzeNKI(directed=False, thresholds=[10,50,90],gpickle_dir='./gpickle_data/'):
    ''' ANALYSIS OF NKI BRAIN ATLAS DATA

    UNDIRECTED INTERPRETATION COMPUTATIONS
    The following calculations are applicable to an undirected reading of
    nki brain atlas data:
        - density
        - clustering
        - topological hierarchy (clustering coefficient vs degree)
            - r2 values for best fit between above
        - number of cliques
        - maximum clique size
        - load centrality
        - number of strongly connected components
        - diameter

    DIRECTED INTERPREATION COMPUTATIONS
    The following additional calculations are run for the directed reading of
    nki brain atlas data:
        - weakly connected components
    the following calculations are not run for directed readings:
        - clique
        - strong conneccted components
    '''
    GPICKLES = os.listdir(gpickle_dir)

    csv = open("resultsDirected-{}.csv".format(directed), "w")

    if not directed:
        csv.write('session_id,session_number,threshold,density, avg_clst, \
                  avg_deg, r2, diameter, num_clq, max_clq_size, max_load_cent, \
                  str connected comps \n')
    else:
        csv.write('session_id,session_number,threshold,density, avg_clst, \
                  avg_deg, r2, diameter, max_load_cent, weak_concomp,\n')

    for threshold in thresholds:
        for gp in GPICKLES:

            G = dMRI2nx('./gpickle_data/{}'.format(gp), threshold=threshold,
                        directed=directed)

            subject_id = gp.split("_")[0]                        # extract id
            session_number = gp.split("ses-")[1].split("_")[0]   # extract sess

            density, avg_clustering, avg_deg, r2, diameter, load_cent = baseCalcs(G)

            if not directed: # we are done; save to csv
                num_clq = len(nx.number_of_cliques(G))
                max_clq_size = nx.graph_clique_number(G)
                strong_concomp = nx.number_connected_components(G)

                csv.write('{},{},{},{:.4f},{:.4f},{},{:.4f},{},{},{},{},{}\n'.format(
                    subject_id, session_number, threshold, density,
                    avg_clustering, avg_deg, r2, diameter, num_clq, max_clq_size,
                    load_cent, strong_concomp))


            elif directed: # there are a few more computations worth checking
                weak_concomp = nx.number_weakly_connected_components(G)

                csv.write('{},{},{},{:.4f},{:.4f},{},{:.4f},{},{},{}\n'.format(
                    subject_id, session_number, threshold, density,
                    avg_clustering, avg_deg, r2, diameter, load_cent, weak_concomp))
    csv.close()


def baseCalcs(G):
    ''' BASIC CALCULATIONS
    the list of these calculations can be found in nkiAnalyze docstring
    '''
    cn_values = []
    dg_values = []

    density = nx.density(G)
    avg_clustering = nx.average_clustering(G)

    clst_nodes = nx.clustering(G)
    deg_nodes = G.degree()

    for value in clst_nodes.values():
        cn_values.append(value)

    for i in deg_nodes:
        dg_values.append(i[1])

    avg_deg = sum(dg_values)//len(dg_values)

    best_fit = np.poly1d(np.polyfit(dg_values, cn_values, 1))
    r2 = r2_score(cn_values, best_fit(dg_values))

    try:
        diameter = nx.diameter(G)
    except:
        diameter = 0

    load_cent = nx.load_centrality(G)
    load_cent = sorted(load_cent.items())
    load_cent = load_cent[0][1]


    return density, avg_clustering, avg_deg, r2, diameter, load_cent


analyzeNKI(False, thresholds=[10,25,50,75,90])
