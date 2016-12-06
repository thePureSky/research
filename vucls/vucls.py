#! /usr/bin/env python
# -*- coding: utf-8 -*-

from scipy import optimize
import math
import json


uploaders = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"]
viewers = [100, 95, 90, 85, 80, 2, 7, 10, 15, 20]

# the numbers of uploaders
n_uploader = len(uploaders)
n_viewers = len(viewers)

# used to store the bitrate of uploaders
up_bitrates = [1.0 for i in range(n_uploader)]

# minimum and maximum of bitrate
r_min = 0.6
r_max = 5
a = math.log(2.0)
r_whole = 20
# step size
ss = 0.01

# the multipliers of the iteration
my_alpha = [0.1 * viewers[i] for i in range(n_uploader)]
my_beta = [1 for i in range(n_uploader)]
my_gamma = 1

# the price
#c = [0.06/12 for i in range(n_uploader)]
c = [0.06/12 for i in range(n_uploader)]


# store the value of L
pre_L =  -100000000

# the value of L
L_h = []

def key_func(x, n):
#	n = 0
#	return (1 / (viewers[n]*(math.log10(1 + x/r_min) - a)*(r_min + x))) - my_alpha[n] + my_beta[n] + my_gamma
#	return (viewers[n] / ((math.log(1 + x/r_min) - a)*(r_min + x))) - my_alpha[n] + my_beta[n] + my_gamma
#	return  (math.log(1 + x/r_min) - a)*(x + r_min) -(viewers[n] / (my_alpha[n] - my_beta[n] - my_gamma))
	return (viewers[n] - c[n]*(x + r_min))/((viewers[n]*(math.log(1 + x/r_min) - a)-c[n] * (x - r_min))*(x + r_min)) - my_alpha[n] + my_beta[n] + my_gamma

def solve_r1():
#	r = optimize.newton(key_func, 0.1)
	r = optimize.fsolve(key_func, 1.0, 0)
	print r[0]
	print key_func(r[0], 0)
	
def solve_r2():
	for i in range(n_uploader):
		r = optimize.fsolve(key_func, 1.0, 0)
		up_bitrates[i] = r[0]
		print r
		print key_func(r[0], 0)
	print_up_bitrates()
	print "The value of L function:", calculate_L()

def solve_r3():
	for j in range(1000):
		for i in range(n_uploader):
			r = optimize.fsolve(key_func, 1, i)[0]
			if r < r_min:
				r = r_min
			if r > r_max:
				r = r_max
			up_bitrates[i] = r
		print_up_bitrates()
		print "iters:", j, "sum:", sum(up_bitrates)
		update_multipliers()
		print_up_bitrates()
		L_value = calculate_L()
		L_h.append(L_value)
		print "The value of L:", L_value
		if abs(L_value - pre_L) < 1.0:
			print "stop!!!!!!!!!!!!!!!"
			break

def calculate_L():
	L = 0.0
	for i in range(n_uploader):
		temp = up_bitrates[i]
		L += math.log(viewers[i]*(math.log(1 + temp/r_min) - a) + c[i]*(temp - r_min)) + my_alpha[i]*(r_min - temp) + my_beta[i]*(temp - r_max) + my_gamma * temp
	L -= my_gamma * r_whole
	return L

def update_multipliers():
	global ss, my_gamma
	print "pre-multipliers:", my_alpha, my_beta, my_gamma
	ss_cur =  ss;
	for i in range(n_uploader):
		my_alpha[i] = max(0, my_alpha[i] + ss_cur * (r_min - up_bitrates[i])) 
	for i in range(n_uploader):
		my_beta[i] = max(0, my_beta[i] + ss_cur * (up_bitrates[i] - r_max)) 
	my_gamma = max(0, my_gamma + ss_cur * (sum(up_bitrates) - r_whole))
	print "post-multipliers:", my_alpha, my_beta, my_gamma
	

def print_up_bitrates():
	print "Here print the bit-rates of uploaders:"
	for i in range(n_uploader):
		print i, up_bitrates[i]

#solve_r1()
#solve_r2()
solve_r3()

with open("L.csv", 'w') as f:
	f.write(json.dumps(L_h) + "\n")

#print_up_bitrates()
