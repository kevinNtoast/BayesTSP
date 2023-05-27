# -*- coding: utf-8 -*-

import scipy.io as sio
import math
import numpy as np
import os
from scipy.spatial.distance import cdist, pdist,squareform

np.set_printoptions(suppress=True)


def tour_distance(order, xys):
    n_city = len(order)
    b = np.ones((n_city, n_city))
    b = b * 999

    for k, i in enumerate(range(n_city)):

        for j in range(i, n_city):
            if order[i] == order[j]:
                continue
            b[k, order[j] - 1] = math.dist(xys[order[i] - 1], xys[order[j] - 1])

    return b


def nn(start, coords):
    dists = squareform(pdist(coords))
    tour = [start]
    visited = np.ones(dists.shape[0],dtype = bool)
    visited[start] = False

    for i in range(dists.shape[0]-1):
        last = tour[-1]
        next_ind = np.argmin(dists[last][visited]) # find minimum of remaining locations
        next_loc = np.arange(dists.shape[0])[visited][next_ind] # convert to original location
        tour.append(next_loc)
        visited[next_loc] = False

    return tour

def tour_length(order, xy):
    length = 0
    for i in range(len(order)):
        if i < max(range(len(order))):
            length += math.dist(xy[i],xy[i+1])
        else:
            length += math.dist(xy[i], xy[0])
    return length


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
city_counts = [3, 4]#[3, 4]        # 3 -> 30 cities, 4 -> 40 cities
s_number = range(82)     # 1~82
p_number = range(9)     # 1~9
l = "1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30"
l2 = "1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40"
a30 = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30]
a40 = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40]

optimal = [14.243350539588022,15.015146397200189,14.197327688886249,14.841307052212043,15.16719209390613,15.063347310424822,13.648941395710613,16.19609437059081,16.613876807479617]

for city in city_counts: 
    for problem in p_number:
        city_out =f"city{city}0_rand"
        if not os.path.isdir(city_out):
            os.mkdir(city_out)

        coords = data_big[city+2][0][problem].tolist()
        nearest = []
        out = []
        # for i in range(city*10):
        #     nearest.append(nn(i,coords))
        #     print(tour_distance(nearest[-1], coords)[:(city*10-2), :])
        #     out.append(tour_distance(nearest[-1], coords)[:(city*10-2), :])
        # print(out.shape)
        # # print(visit_order)
        # # print(coords)
        # # print(nearest)
        # # print(coords)

        # print(nearest.shape)
        # print(out.shape)
        if city == 3:
            for i in range(city*10):
                bryce = i if i >= 10 else '0' + str(i)
                np.random.shuffle(a30)
                out = tour_distance(a30, coords)[:28, :]
                np.savetxt(f"{city_out}/dist30_random_prob{problem}_{bryce}.csv", out, delimiter=',', fmt='%f',header = l)
                np.savetxt(f"{city_out}/solution/sol{city}0_random_prob{problem}_{bryce}.csv", np.transpose(a30)[1:29],
                           delimiter=',', fmt='%f', header='order')
        else:
            for i in range(city*10):
                bryce = i if i >= 10 else '0' + str(i)
                np.random.shuffle(a40)
                out = tour_distance(a40, coords)[:38, :]
                np.savetxt(f"{city_out}/dist40_random_prob{problem}_{bryce}.csv", out, delimiter=',', fmt='%f',
                           header=l2)
                np.savetxt(f"{city_out}/solution/sol{city}0_random_prob{problem}_{bryce}.csv", np.transpose(a40)[1:39],
                           delimiter=',', fmt='%f', header='order')
