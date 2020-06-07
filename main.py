from analyzeNKI import analyzeNKI
from degDist import degDist

thresholds = [10,20,30,40,50,60,70,80,90]

analyzeNKI(directed=False,thresholds=thresholds,gpickle_dir='./gpickle_data/')
degDist(gpickle_dir='./gpickle_data/', thresholds=thresholds)
