'''GA迷宫寻路'''
'''python速成太难了'''

import numpy as np
from sko.GA import GA

# 迷宫的矩阵表示，1代表障碍物
map = [[1,1,1,1,1,1,1],
       [1,0,0,0,0,0,1],
       [1,0,1,0,1,1,1],
       [1,0,0,0,0,0,1],
       [1,0,1,0,1,1,1],
       [1,0,1,0,0,0,1],
       [1,1,1,1,1,1,1]]

add = [[-1, 0], [0, 1], [1, 0], [0, -1]] # 上右下左四个方向上移动时行和列的增量

rNum = len(map) - 2     # 行数
cNum = len(map[0]) - 2  # 列数
star = [3, 1]           # 起点
end = [5, 5]            # 终点
minTry = ( end[0] - star[0] ) + ( end[1] - star[1] ) # 寻路起始步数

def demo_func(p):

    now = [3, 1]      # 起点

    for operand in p:                 # 读取移动步骤，移动当前位置
        if(map[now[0]][now[1]] == 1): # 碰到墙壁，返回无穷大
            return float('inf')
        now[0] += add[int(operand)][0]
        now[1] += add[int(operand)][1]

    return abs(end[0] - now[0]) + abs(end[1] - now[1]) + 1e-7

def findWay(tryNum): # 找从起点移动tryNum步距终点最近的路径
    lBoundary = []   # 存自变量下界
    uBoundary = []   # 存自变量上界
    precisions = []  # 存自变量精度

    for i in range(tryNum): # 0，1，2，3代表四个方向，从0到3，精度为1
        lBoundary.append(0)
        uBoundary.append(3)
        precisions.append(1)

    ga = GA(func=demo_func, n_dim=tryNum, size_pop=150, max_iter=1000, lb=lBoundary, ub=uBoundary, precision=precisions)
    return ga.run()

def star(): # 返回移动步骤
    for tryNum in range(minTry, minTry + rNum + cNum):   # 尝试走minTry步找到出口，最多走minTry + rNum + cNum步
        best_operations, best_distance = findWay(tryNum)
        if(best_distance < 0.5):
            print("移动步骤：" + str(best_operations))   # 可注释
            return best_operations

def testGA(testNum): # 测试testNum次，计算6步找到出口的成功率
    right = 0        # 测试成功次数
    test_result = [] # 存放测试结果

    for i in range(testNum):  # 得到最短路径（所有结果最小值）和测试结果
        tryNum = len(star())
        test_result.append(tryNum)
        if(i == 0):
            best_result = tryNum
        elif(best_result > tryNum):
            best_result = tryNum

    for result in test_result: # 遍历测试结果，得到测试成功次数
        if(result == best_result):
            right += 1

    print("成功率：{}".format(right / testNum))

testGA(100)
