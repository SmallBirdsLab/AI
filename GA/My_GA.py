'''遗传算法求函数最值'''
'''x^2在[0,31]上最大值，一个染色体包含5位基因'''
'''包含了测试'''
import matplotlib.pyplot as plt
import numpy as np
import random

# (-1, 2)
# 初始化原始种群
def ori_popular1(num):
    popular = []
    for i in range(num):
        x = random.randint(0, 31)  # 在此范围内生成一个随机浮点数
        popular.append(x)
    return popular

# 编码，也就是由表现型到基因型，性征到染色体
def encode(popular, gene_num):  # popular应该是int类型的列表
    popular_gene = []
    for data in popular:
        bin_data = bin( data )  # 整形转换成二进制是以字符串的形式存在的
        for j in range(len(bin_data)-2, gene_num):  # 序列长度不足补0
            bin_data = bin_data[0:2] + '0' + bin_data[2:]
        popular_gene.append(bin_data)
    return popular_gene

# 解码，即适应度函数。通过基因，即染色体得到个体的适应度值
def decode(popular_gene, gene_num):
    fitness = []
    for i in range(len(popular_gene)):
        x = int(popular_gene[i], 2) # 解码为实数
        value = x * x + 0.0001               # 计算适应度
        fitness.append(value)
    return fitness

# 选择and交叉。选择用轮牌赌，交叉概率为0.66
def choice(popular_gene, gene_num):
    fitness = decode(popular_gene, gene_num)
    sum_fit_value = 0
    for i in range(len(fitness)):
        sum_fit_value += fitness[i]
    # 各个个体被选择的概率
    probability = []
    for i in range(len(fitness)):
        probability.append(fitness[i]/sum_fit_value)
    # 概率分布
    probability_sum = []
    probability_sum.append(probability[0])
    for i in range(1, len(fitness)):
            probability_sum.append(probability_sum[i-1] + probability[i])

    # 选择
    popular_new = []
    for i in range(int(len(fitness)/2)):
        for j in range(2): # 2个2个的选
            rand = random.uniform(0, 1)  # 在0-1之间随机一个浮点数
            for k in range(len(fitness)):
                if (k == 0 and rand < probability_sum[k]):
                        popular_new.append(popular_gene[k])
                elif (rand > probability_sum[k-1]) and (rand < probability_sum[k]):
                        popular_new.append(popular_gene[k])
    return popular_new

# 交叉，交叉率为pc。
def cross(popular_old, gene_num, pc):
    for i in range(0, len(popular_old), 2):
        is_change = random.random()
        if is_change <= pc:
            temp_s = popular_old[i][int(gene_num / 2) + 3:]
            popular_old[i] = popular_old[i][0:int(gene_num / 2) + 3] + popular_old[i+1][int(gene_num / 2) + 3:]
            popular_old[i+1] = popular_old[i+1][0:int(gene_num / 2) + 3] + temp_s

# 变异.概率为pv
def variation(popular_new, gene_num, pv):
    for i in range(len(popular_new)):
        is_variation = random.uniform(0, 1)
        if is_variation <= pv:
            rand = random.randint(2, gene_num + 1) # rand位置的数加1对2取余
            popular_new[i] = popular_new[i][0:rand] + str((int(popular_new[i][rand])+1)%2) + popular_new[i][rand+1:]
    return popular_new

def run(p):      # 传入参数p进行测试
    gene_num = 5 # 染色体上基因个数
    '''在此修改被p赋值修改的参数'''
    num = 22     # 种群数量
    pc = 0.7     # 交叉概率
    pv = p       # 变异概率

    ori_popular = ori_popular1(num)                  # 初始化原始种群,
    ori_popular_gene = encode(ori_popular, gene_num) # 得到原始种群的基因
    new_popular_gene = ori_popular_gene

    tryNum = 1
    best_fitness = float("-inf")
    while( best_fitness < 961):  # 当找到最优解时跳出循环
        new_popular_gene = choice(new_popular_gene, gene_num)# 选择
        cross(new_popular_gene, gene_num,pc)
        new_popular_gene = variation(new_popular_gene, gene_num, pv)   # 变异

        # 取当代所有个体适应度平均值
        new_fitness = decode(new_popular_gene, gene_num)
        best_fitness = new_fitness[0]
        for j in new_fitness:
            #sum_new_fitness += j
            if(best_fitness < j):
                best_fitness = j

        tryNum += 1

    return tryNum

# 画图
x = np.arange(0.005, 1.005, 0.005) # 横坐标，传入参数
y = []                             # 纵坐标，测试结果

for testX in x:
    exper = 0
    for i in range(10000): # 测试多次遍取平均值
        exper += run(testX)
    y.append( exper / 10000 )
    print('x: ', testX, '   y: ', exper / 10000)

fig = plt.figure()  # 相当于一个画板
axis = fig.add_subplot(111)  # 坐标轴
axis.plot(x, np.array(y))
plt.show()
