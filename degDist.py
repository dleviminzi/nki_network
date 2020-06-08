import networkx as nx
from sklearn.metrics import r2_score
import collections
import os
import csv
from dMRI2nx import dMRI2nx
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import powerlaw
'''
def degDist(thresholds, gpickle_dir='./gpickle_data/'):
    GPICKLES = os.listdir(gpickle_dir)

    for threshold in thresholds:
        for gp in GPICKLES:
            G = dMRI2nx('./gpickle_data/{}'.format(gp), threshold=threshold,
                         directed=False)'''


def degDist(G, subject_id, session_number,threshold):
    degree_sequence = sorted([d for n, d in G.degree()], reverse=True)
    degreeCount = collections.Counter(degree_sequence)
    deg, cnt = zip(*degreeCount.items())

    total_cnt = 0
    for i in cnt:
        total_cnt += i

    ct = []
    for i in cnt:
        ct.append(i/total_cnt)

    P_k = []
    for i in range(len(ct)):
        x = ct[i]
        j = i
        while j < len(cnt):
            x += ct[j]
            j += 1
        P_k.append(x)

    P_k = P_k[::-1]

    best_fit = np.poly1d(np.polyfit(np.log10(deg), np.log10(P_k), 1))
    r2 = r2_score(np.log10(P_k), best_fit(np.log10(deg)))

    fig, ax = plt.subplots(figsize=(20, 10))
    plt.plot(np.log10(deg),np.log10(P_k),'yo',np.log10(deg),best_fit(np.log10(deg)),'--k')
    plt.title('{}-{}-{} Powerlaw Adherence r2: {}'.format(subject_id,session_number,threshold,r2))
    plt.xlim(0,2)
    plt.ylabel("P_k")
    plt.xlabel("Degree")
    plt.savefig('./degreeDist/{}-{}-{}.png'.format(subject_id, session_number, threshold))
    plt.close()

    return r2


    ''' OLD - USE FOR GETTING PLAIN DEGREE DISTRIBUTION
            fig, ax = plt.subplots(figsize=(20, 10))
            plt.bar(deg, cnt, width=0.80, color='b')
            plt.title("Degree Histogram - {} {} {}".format(subject_id, session_number, threshold))
            plt.ylabel("Count")
            plt.xlabel("Degree")
            ax.set_xticks([d + 0.4 for d in deg])
            ax.set_xticklabels(deg)

            plt.savefig('./degreeDist/{}-{}-{}.png'.format(subject_id, session_number, threshold))
            plt.close()

            csv = open("./degreeDist/raw{}/dD{}-{}-{}.csv".format(threshold, threshold, subject_id, session_number), "w")
            csv.write('sub{},ses{},\n'.format(subject_id, session_number))
            csv.write('degree,count,\n')

            for d,c in degreeCount.items():
                csv.write('{},{},\n'.format(d,c))

            for i in range(8):         # very lazy fix
                csv.write('0,0,\n')


            csv.close()


    for threshold in thresholds:
        raw = os.listdir('./degreeDist/raw{}'.format(threshold))
        paste_str = ''

        for file in raw:
            paste_str += './degreeDist/raw{}/'.format(threshold) + file + ' '

        os.system('paste {} > ./degreeDist/dD{}.csv'.format(paste_str, threshold))
    '''

