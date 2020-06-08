from analyzeNKI import analyzeNKI
from degDist import degDist

thresholds = [1,10,20,30,40,50,60,70,80,90,92.5,95,97.5]

#analyzeNKI(thresholds, directed=False, gpickle_dir='./gpickle_data/')
degDist(thresholds, gpickle_dir='./gpickle_data/')
