# -*- coding: utf-8 -*-

import scipy.io as sio
import math
import numpy as np
import os
from scipy.spatial.distance import cdist, pdist,squareform
import pylab as pl
from matplotlib import collections as mc

np.set_printoptions(suppress=True)


def makepath(order, coord):
    ret = []
    for i in range(len(order)):
        if i < len(order)-1:
            ret.append([ coord[order[i]-1], coord[order[i+1]-1] ])
        else:
            ret.append([ coord[order[i]-1], coord[order[0]-1] ])
    return ret



mat=sio.loadmat('data.mat')# load mat-file
# print(type(mat))

data_big = mat['tsp'][0][0]
"""
(1, 1)          nSubjects
(1, 1)          nProblems30
(1, 1)          nProblems40
(30, 9, 82)     tours30
(40, 9, 82)     tours40
(1, 9)          coords30
(1, 9)          coords40
"""
city_counts = [4]        # 3 -> 30 cities, 4 -> 40 cities
s_number = range(82)     # 1~82
p_number = range(9)     # 1~9
l = "1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30"
l2 = "1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40"

for city in city_counts:
    for problem in p_number:
        city_out =f"city{city}0_img"
        if not os.path.isdir(city_out):
            os.mkdir(city_out)

        for subject in s_number:
            visit_order = data_big[city][:,problem,subject]
            coords = data_big[city+2][0][problem].tolist()

            path = makepath(visit_order, coords)
            z = np.array(coords)
            x,y = z.T

            lc = mc.LineCollection(path, linewidths=2)
            fig, ax = pl.subplots()
            ax.add_collection(lc)
            ax.autoscale()
            ax.margins(0.1)
            pl.scatter(x,y)
            pl.axis('off')
            pl.savefig(f"{city_out}/{city}0_sub{subject}_prob{problem}.png")
            pl.clf()
            pl.close('all')
            pl.cla()
