import numpy as np
from scipy import spatial
import pandas as pd

from sko.GA import GA_TSP

num_points = 5 # 城市数量

# 城市的矩阵表示
map = [ [0      ,1462   ,3179   ,3179   ,1165],
        [1462   ,0.     ,1811   ,2677   ,1511],
        [3179   ,1811   ,0.     ,2216   ,2129],
        [3179   ,2677   ,2216   ,0      ,1942],
        [1165   ,1511   ,2129   ,1942   ,0   ] ]
distance_matrix = np.array(map)

def cal_total_distance(routine):
    num_points, = routine.shape
    return sum([distance_matrix[routine[i % num_points], routine[(i + 1) % num_points]] for i in range(num_points)])

def runGA():
    ga_tsp = GA_TSP(func=cal_total_distance, n_dim=num_points, size_pop=8, max_iter=10, prob_mut=0.1)
    return ga_tsp.run()

def testGA(testNum): # 测试testNum次，计算找到最短路径的成功率
    right = 0        # 测试成功次数
    test_result = [] # 存放测试结果

    for i in range(testNum): # 得到最短路径（所有结果最小值），测试结果
        points, distance = runGA()
        print(points)
        print(distance)
        test_result.append(distance)
        if(i == 0):
            best_distance = distance
        elif(best_distance > distance):
            best_distance = distance

    for i in range(testNum): # 得到测试成功次数
        if(test_result[i] == best_distance):
            right += 1

    print("成功率：{}".format(right / testNum))

testGA(1000)
