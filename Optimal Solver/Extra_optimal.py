# -*- coding: utf-8 -*-

import scipy.io as sio
import math
import numpy as np
import os
from scipy.spatial.distance import cdist, pdist,squareform
from python_tsp.exact import solve_tsp_dynamic_programming
from python_tsp.distances import great_circle_distance_matrix
from python_tsp.heuristics import solve_tsp_simulated_annealing

np.set_printoptions(suppress=True)

#problems
p1 = np.array([[0.0238,	0.6136],[0.1088,	0.7669],[0.549,	0.3713],[0.0861,	0.3345],[0.5985,	0.2163],[0.8208,	0.5711],[0.8166,	0.0282],[0.237,	0.0169],[0.6454,	0.2927],[0.4397,	0.67],[0.1533,	0.618],[0.1125,	0.4996],[0.4954,	0.9741],[0.3274,	0.3365],[0.7894,	0.927],[0.2129,	0.6968],[0.9082,	0.2222],[0.6224,	0.8328],[0.6567,	0.7573],[0.9258,	0.4472],[0.4893,	0.4814],[0.3378,	0.7087],[0.463,	0.5362],[0.2884,	0.0195],[0.5427,	0.7604],[0.9331,	0.3756],[0.8535,	0.9406],[0.3048,	0.7735],[0.371,	0.5046],[0.5136,	0.6952]])
p2 = np.array([[0.3906,	0.9006],[0.7733,	0.1350],[0.5476,	0.5041],[0.9893,	0.6572],[0.7206,	0.0166],[0.6072,	0.5869],[0.8310,	0.2363],[0.5450,	0.2326],[0.7662,	0.0639],[0.4132,	0.8256],[0.6448,	0.7056],[0.9052,	0.3480],[0.3326,	0.1268],[0.4380,	0.6113],[0.2082,	0.7543],[0.0429,	0.5839],[0.1782,	0.4304],[0.5061,	0.9698],[0.9435,	0.6153],[0.5144,	0.8405],[0.5205,	0.6928],[0.9763,	0.4120],[0.1840,	0.8176],[0.5056,	0.3634],[0.9621,	0.8373],[0.6351,	0.6587],[0.2745,	0.5546],[0.7696,	0.6460],[0.3899,	0.2261],[0.9517,	0.7602]])
p3 = np.array([[0.9837,	0.3859],[0.3987,	0.3897],[0.2664,	0.2745],[0.7731,	0.3956],[0.1114,	0.4018],[0.6541,	0.2136],[0.5237,	0.8155],[0.7113,	0.3978],[0.1538,	0.6266],[0.4236,	0.0736],[0.9382,	0.075],[0.8454,	0.6406],[0.9704,	0.9221],[0.6216,	0.7262],[0.7409,	0.8993],[0.2539,	0.3881],[0.3286,	0.6657],[0.6159,	0.5682],[0.2408,	0.822],[0.7187,	0.795],[0.2041,	0.2506],[0.7271,	0.1372],[0.4807,	0.5853],[0.7293,	0.6116],[0.4596,	0.6593],[0.3503,	0.5942],[0.3495,	0.3101],[0.6864,	0.9708],[0.3147,	0.3795],[0.8329,	0.7173]])
p4 = np.array([[0.2331,	0.7726],[0.8344,	0.2954],[0.9105,	0.258],[0.0746,	0.7353],[0.3598,	0.8538],[0.7066,	0.8315],[0.3437,	0.334],[0.2204,	0.6773],[0.8955,	0.6614],[0.5401,	0.062],[0.9595,	0.0653],[0.7905,	0.1743],[0.2819,	0.3698],[0.3119,	0.5556],[0.5513,	0.5716],[0.9262,	0.3029],[0.7891,	0.6688],[0.4522,	0.522],[0.9907,	0.7383],[0.4716,	0.0304],[0.0153,	0.2642],[0.7274,	0.7162],[0.4742,	0.7147],[0.3867,	0.3771],[0.8246,	0.9136],[0.2892,	0.4217],[0.6843,	0.6044],[0.6577,	0.2442],[0.6826,	0.4611],[0.7822,	0.037]])
p5 = np.array([[0.9275,	0.5085],[0.1063,	0.2281],[0.3046,	0.187],[0.8913,	0.6614],[0.8897,	0.0268],[0.8372,	0.6784],[0.5244,	0.3154],[0.6435,	0.4931],[0.6294,	0.6032],[0.2217,	0.6837],[0.5326,	0.7189],[0.6482,	0.3331],[0.0474,	0.0352],[0.3677,	0.4201],[0.3005,	0.9841],[0.8103,	0.8232],[0.2737,	0.392],[0.3289,	0.932],[0.5781,	0.7108],[0.7873,	0.0716],[0.8648,	0.9848],[0.1084,	0.1107],[0.1153,	0.0041],[0.8175,	0.3751],[0.3966,	0.1869],[0.4393,	0.2493],[0.8056,	0.1154],[0.4374,	0.1546],[0.6405,	0.2075],[0.302	,0.5738],])
p6 = np.array([[0.6878,	0.6711],[0.5377,	0.4264],[0.4824,	0.5857],[0.1497,	0.7733],[0.4229,	0.7158],[0.4042,	0.5747],[0.5441,	0.6308],[0.0737,	0.5733],[0.7771,	0.4955],[0.0384,	0.2528],[0.2682,	0.6836],[0.7399,	0.6005],[0.1177,	0.7064],[0.207,	0.8432],[0.7084,	0.2285],[0.0082,	0.5872],[0.2833,	0.3334],[0.4554,	0.2096],[0.7736,	0.0393],[0.0568,	0.4986],[0.8776,	0.0644],[0.2198,	0.544],[0.388,	0.843],[0.7705,	0.7907],[0.3266,	0.8664],[0.9916,	0.82],[0.4108,	0.3476],[0.597,	0.1064],[0.4934,	0.525],[0.0398,	0.1034]])
p7 = np.array([[0.4366,	0.514],[0.054,	0.8049],[0.3768,	0.3753],[0.6745,	0.5806],[0.3888,	0.5721],[0.6361,	0.2897],[0.7294,	0.3962],[0.876,	0.6836],[0.4573,	0.7341],[0.5471,	0.8659],[0.5736,	0.6452],[0.2836,	0.4962],[0.4123,	0.1899],[0.7171,	0.2429],[0.2416,	0.486],[0.3519,	0.1452],[0.0296,	0.2707],[0.8015,	0.6344],[0.2023,	0.321],[0.821,	0.4402],[0.1627,	0.442],[0.7014,	0.3187],[0.9706,	0.6125],[0.9072,	0.0494],[0.4813,	0.7974],[0.4514,	0.37],[0.9093,	0.5937],[0.0716,	0.7326],[0.4031,	0.6184],[0.7291,	0.815]])
p8 = np.array([[0.5176,	0.5948],[0.2158,	0.9822],[0.2324,	0.5207],[0.4765,	0.3351],[0.0187,	0.877],[0.5123,	0.1634],[0.9765,	0.9257],[0.8497,	0.9502],[0.4687,	0.1408],[0.3794,	0.0861],[0.1364,	0.1614],[0.4968,	0.4469],[0.1648,	0.9944],[0.4932,	0.2217],[0.7986,	0.4683],[0.1076,	0.936],[0.8582,	0.0569],[0.0026,	0.2279],[0.3022,	0.0162],[0.5007,	0.855],[0.3069,	0.5941],[0.2411,	0.4621],[0.2504,	0.7188],[0.9999,	0.8514],[0.9599,	0.3335],[0.0526,	0.5627],[0.0579,	0.6454],[0.7991,	0.7768],[0.9645,	0.7266],[0.4022,	0.6767]])
p9 = np.array([[0.4095,	0.3488],[0.7895,	0.3794],[0.811,	0.0995],[0.9212,	0.0821],[0.6592,	0.9361],[0.518,	0.2215],[0.7011,	0.6797],[0.9292,	0.3126],[0.7045,	0.0898],[0.6883,	0.3166],[0.098,	0.9427],[0.2795,	0.3442],[0.8623,	0.3591],[0.1524,	0.6085],[0.6701,	0.383],[0.9883,	0.6284],[0.2776,	0.809],[0.2154,	0.6816],[0.1641,	0.261],[0.7748,	0.5076],[0.4236,	0.52],[0.5614,	0.7148],[0.6015,	0.0883],[0.6247,	0.7127],[0.2945,	0.1989],[0.9735,	0.8733],[0.4407,	0.1257],[0.3468,	0.5427],[0.3147,	0.1076],[0.8399,	0.9975]])

dm1 = great_circle_distance_matrix(p1)
dm2 = great_circle_distance_matrix(p2)
dm3 = great_circle_distance_matrix(p3)
dm4 = great_circle_distance_matrix(p4)
dm5 = great_circle_distance_matrix(p5)
dm6 = great_circle_distance_matrix(p6)
dm7 = great_circle_distance_matrix(p7)
dm8 = great_circle_distance_matrix(p8)
dm9 = great_circle_distance_matrix(p9)

e1, d1 = solve_tsp_simulated_annealing(dm1)
e2, d2 = solve_tsp_simulated_annealing(dm2)
e3, d3 = solve_tsp_simulated_annealing(dm3)
e4, d4 = solve_tsp_simulated_annealing(dm4)
e5, d5 = solve_tsp_simulated_annealing(dm5)
e6, d6 = solve_tsp_simulated_annealing(dm6)
e7, d7 = solve_tsp_simulated_annealing(dm7)
e8, d8 = solve_tsp_simulated_annealing(dm8)
e9, d9 = solve_tsp_simulated_annealing(dm9)

ff = [
    [x + 1 for x in e1],
    [x + 1 for x in e2],
    [x + 1 for x in e3],
    [x + 1 for x in e4],
    [x + 1 for x in e5],
    [x + 1 for x in e6],
    [x + 1 for x in e7],
    [x + 1 for x in e8],
    [x + 1 for x in e9]]

print(ff)



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
city_counts = [3]#[3, 4]        # 3 -> 30 cities, 4 -> 40 cities
s_number = range(82)     # 1~82
p_number = range(9)     # 1~9
l = "1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30"
l2 = "1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40"
a30 = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30]
a40 = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40]

optimal = [14.243350539588022,15.015146397200189,14.197327688886249,14.841307052212043,15.16719209390613,15.063347310424822,13.648941395710613,16.19609437059081,16.613876807479617]
# os.mkdir("optimal")
# os.mkdir("optimal/solution")
for city in city_counts: 
    for problem in p_number:
        # city_out =f"city{city}0_rand"
        # if not os.path.isdir(city_out):
        #     os.mkdir(city_out)

        coords = data_big[city+2][0][problem].tolist()
        # nearest = []
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

                out = tour_distance(ff[problem], coords)[:28, :]
                np.savetxt(f"optimal/dist{problem}.csv", out, delimiter=',', fmt='%f',header = l)
                np.savetxt(f"optimal/solution/sol_optimal_{problem}.csv", np.transpose(ff[problem])[1:29],
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
