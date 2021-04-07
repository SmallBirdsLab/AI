import numpy as np
from sko.GA import GA

'''求f(x) = x ^ 2在[0, 31]上的最大值'''
t = 0.0001
def demo_func(p):
    x1, = p
    return 1.0 / (np.square(x1) + t)

ga = GA(func=demo_func, n_dim=1, size_pop=50, max_iter=800, lb=[0], ub=[31], precision=1e-7)
best_x, best_y = ga.run()
print('best_x:', best_x, '\n', 'best_y:', best_y)
