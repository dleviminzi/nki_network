import matplotlib.pyplot as plt
from dMRI2nx import dMRI2nx
import networkx as nx
import collections
import os

def degDist(gpickle_dir='./gpickle_data/', thresholds=[10,50,90]):
    GPICKLES = os.listdir(gpickle_dir)

    for threshold in thresholds:
        for gp in GPICKLES:
            G = dMRI2nx('./gpickle_data/{}'.format(gp), threshold=threshold,
                         directed=False)
            degree_sequence = sorted([d for n, d in G.degree()], reverse=True)
            degreeCount = collections.Counter(degree_sequence)
            deg, cnt = zip(*degreeCount.items())

            subject_id = gp.split("_")[0]
            session_number = gp.split("ses-")[1].split("_")[0]

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


degDist()
