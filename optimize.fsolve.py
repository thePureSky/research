# -*- coding: utf-8 -*-

from scipy import special, optimize
import math

def f(x):
	return 1/(math.log10(x)) - 3

sol = optimize.fsolve(f, 2.0)


print sol

