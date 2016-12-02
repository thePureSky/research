#! /usr/bin/env python
# -*- coding: utf-8 -*-

from scipy import optimize
import math


uploaders = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"]
viewers = [100, 95, 90, 85, 80, 2, 7, 10, 15, 20]

# the numbers of uploaders
n_uploader = len(uploaders)
n_viewers = len(viewers)

# used to store the bitrate of uploaders
up_bitrates = [1.0 for i in range(n_uploader)]

# minimum and maximum of bitrate
r_min = 0.6
r_max = 10
a = math.log(2.0)
r_whole = 20
# step size
ss = 0.001

# the multipliers of the iteration
my_alpha = [3.0 for i in range(n_uploader)]
my_beta = [1.0 for i in range(n_uploader)]
my_gamma = 1.0 

def key_func(x, n):
#	n = 0
#	return (1 / (viewers[n]*(math.log10(1 + x/r_min) - a)*(r_min + x))) - my_alpha[n] + my_beta[n] + my_gamma
#	return (viewers[n] / ((math.log(1 + x/r_min) - a)*(r_min + x))) - my_alpha[n] + my_beta[n] + my_gamma
	return  (math.log(1 + x/r_min) - a)*(x + r_min) -(viewers[n] / (my_alpha[n] - my_beta[n] - my_gamma))
	
def solve_r():
#	r = optimize.newton(key_func, 0.1)
#	r = optimize.fsolve(key_func, 1.0, 0)[0]
	for j in range(1000):
		for i in range(n_uploader):
			r = optimize.fsolve(key_func, 1, i)[0]
#			if r > r_max:
#				r = r_max
#			if r < r_min:
#				r = r_min
			up_bitrates[i] = r
		print "iters:", j, "sum:", sum(up_bitrates)
		update_multipliers()
		print_up_bitrates()

	print_up_bitrates()
	
def calculate_L():
	pass

def update_multipliers():
	print "multipliers:", my_alpha, my_beta, my_gamma

	global ss
	ss_cur =  ss;
	for i in range(n_uploader):
		my_alpha[i] = max(0, my_alpha[i] + ss_cur * (r_min - up_bitrates[i])) 
	for i in range(n_uploader):
		my_beta[i] = max(0, my_beta[i] + ss_cur * (up_bitrates[i] - r_max)) 
	my_gammma = max(0, sum(up_bitrates) - r_whole)
	

#	ss = ss + 1

def print_up_bitrates():
	print "Here print the bit-rates of uploaders:"
	for i in range(n_uploader):
		print i, up_bitrates[i]

solve_r()

#print_up_bitrates()
