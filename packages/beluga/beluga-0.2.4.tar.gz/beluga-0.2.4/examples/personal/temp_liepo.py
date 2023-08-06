from beluga.liepack.domain.liealgebras import *
from beluga.liepack.field import VectorField
from beluga.ivpsol import Flow, RKMK
import numpy as np
from matplotlib import pyplot as plt
from sympy.diffgeom import Manifold, Patch, CoordSystem, WedgeProduct, TensorProduct, Commutator, covariant_order, Differential
from math import floor
from beluga.codegen import make_jit_fn

M = Manifold('M', 2)
P = Patch('P',M)
C = CoordSystem('C', P, names=['x','y'])

coord = C.coord_functions()
dx = C.base_oneforms()
Dx = C.base_vectors()

omega = 0
pi = 0
n = len(coord)

func = coord[0]
hamiltonian = coord[0]**2 + coord[1]**2

for ii in range(floor(n/2)):
    omega += WedgeProduct(dx[ii], dx[ii+floor(n / 2)])
    pi += WedgeProduct(Dx[ii], Dx[ii + floor(n / 2)])

def X_(arg):
    return pi.rcall(None, arg)

def d(f):
    order = covariant_order(f)
    if order == 0:
        return sum([Differential(f)(D_x) * dx for (D_x, dx) in zip(Dx, dx)])

def sharp(f):
    set1d = dict(zip(dx, Dx))
    return f.subs(set1d, simultaneous=True)

def flat(f):
    set1D = dict(zip(Dx, dx))
    return f.subs(set1D, simultaneous=True)

X_x = X_(func)
X_H = X_(hamiltonian)

system = Commutator(sharp(d(func)), sharp(d(hamiltonian)))

the_eoms = [make_jit_fn(coord, flat(system).rcall(D_x)) for D_x in Dx]

breakpoint()


