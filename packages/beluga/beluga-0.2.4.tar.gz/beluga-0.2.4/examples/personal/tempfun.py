from beluga.ivpsol import Trajectory
from beluga.bvpsol import Collocation
import numpy as np
import time
from scipy.special import erf

const = 1e-2


def odefun(X, u, p, const):
    return (2 * X[1], 2 * (((1 + const[0]) * X[0] - X[1]) / const[0]), 2)


def bcfun(X0, q0, u0, Xf, qf, uf, p, ndp, const):
    return (X0[0] - 1 - np.exp(-2), Xf[0] - 1 - np.exp(-2 * (1 + const[0]) / const[0]), X0[2] + 1)

t0 = time.time()
algo = Collocation(odefun, None, bcfun, number_of_nodes_min=10, number_of_nodes_max=100)
solinit = Trajectory()
solinit.t = np.linspace(0, 1, 2)
solinit.y = np.array([[-1, 0, -1], [-1, 0, 1]])
solinit.const = np.array([const])
sol = algo.solve(solinit)
t1 = time.time()
print('Time to sol:\t' + str(t1-t0))
print('Num nodes:\t' + str(len(sol.t)))

import matplotlib.pyplot as plt
plt.plot(sol.t, np.ones(sol.t.size), marker='o')
plt.show()

plt.plot(sol.t, sol.y[:,0], marker='o', linestyle='-')
plt.show()
