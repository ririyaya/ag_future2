"""
DTWDistance(s1, s2) is copied from:
http://alexminnaar.com/2014/04/16/Time-Series-Classification-and-Clustering-with-Python.html
"""
import numpy as np
import math
# import matplotlib.pyplot as plt

def euclid_dist(t1, t2):
    return np.sqrt(np.sum((t1 - t2) ** 2))


# t = np.arange(9)
# ts1 = 5 * np.sin(2 * np.pi * t * 0.05)  # 0.05Hz sin wave, 1Hz sampling rate, amplitude=5
# ts2 = 3 * np.sin(2 * np.pi * t * 0.02)  # 0.02Hz sin wave, 1Hz sampling rate, amplitude=3
# ts3 = 0.08 * t - 4
ts1=[1,3,1,3,5,6]
ts2=[4,2,3,6,3]

def DTWDistance(s1, s2):
    DTW = {}

    for i in range(len(s1)):
        DTW[(i, -1)] = float('inf')
    for i in range(len(s2)):
        DTW[(-1, i)] = float('inf')
    DTW[(-1, -1)] = 0

    for i in range(len(s1)):
        for j in range(len(s2)):
            dist = (s1[i] - s2[j]) ** 2
            DTW[(i, j)] = dist + min(DTW[(i - 1, j)], DTW[(i, j - 1)], DTW[(i - 1, j - 1)])
    # print(DTW)
    return np.sqrt(DTW[len(s1) - 1, len(s2) - 1])


dtw_dist_12 = DTWDistance(ts1, ts2)
# print('dtw_dist_12 = {0:6.2f}'.format(dtw_dist_12))
print(dtw_dist_12)
