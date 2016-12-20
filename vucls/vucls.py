#! /usr/bin/env python
# -*- coding: utf-8 -*-

# using the optimize function from scipy library to get the numerical solution of the derivative
# for example, optimize.fsolve(key_func, 1.0, 1), key_func is function returning th value of the objective, defined as below.
# 1.0 is a initialized value; 1 is the index of uploaders. Then we can get the bir-rate ri of this uploader
from scipy import optimize
import math
import json

# the name of the uploaders
uploaders = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"]
# the number of viewers for each uploader
viewers = [100, 95, 90, 85, 80, 2, 7, 10, 15, 20]

# the numbers of uploaders
n_uploader = len(uploaders)

# used to store the bitrate of uploaders, initialized with 1.0
up_bitrates = [1.0 for i in range(n_uploader)]

# the minimum and maximum of bitrate
r_min = 0.6
r_max = 5

# a constant of ln(2)
a = math.log(2.0)

# the overall bandwidth, that is, the overall bitrate
r_whole = 20


# used to calculate the step size of the subgradient, 1 / ss, that is, 1 / 100 = 0.01, and ss woulb added with 1 each step
ss = 100

# define and initialize the multipliers 
my_alpha = [1 for i in range(n_uploader)]
my_beta = [1 for i in range(n_uploader)]
my_gamma = 2

# the price of the bandwidth, 0.06Mbps/hour, we adopt the time slot as 5 minutes, so the price is 0.06/12
c = [0.06/12 for i in range(n_uploader)]

# store the tuning parameter k, which represents the weight of the bandwidth cost
k = 100

# store the previous value of L, which is the value of the objective
pre_L =  -100000000

# the value of L, used to store all the values of the objective, for post-analysis
L_h = []

# the function of the derivative, n is a parameter representing the index of an uploader.
# for example, if n == 1, means the uploader 1.
def key_func(x, n):
	# return the value of the objective,  the function of (17)
	return (viewers[n] -k * c[n]*(x + r_min))/((viewers[n]*(math.log(1 + x/r_min) - a)-k * c[n] * (x - r_min))*(x + r_min)) + my_alpha[n] - my_beta[n] -  my_gamma

# used to calculate the ri for a single uploader
def solve_r1():
#	r = optimize.newton(key_func, 0.1)
	r = optimize.fsolve(key_func, 1.0, 0)
	print r[0]
	
# used to calculate the ri for all uploaders, but not with iteration
def solve_r2():
	for i in range(n_uploader):
		r = optimize.fsolve(key_func, 1, i)
		up_bitrates[i] = r[0]
		print r
	print_up_bitrates()
	print "The value of L function:", calculate_L()

# used to calculate the ri for all uploaders, with iteration and judge whether stop
def solve_r3():
	for j in range(300):
		for i in range(n_uploader):
			r = optimize.fsolve(key_func, 1.0, i)[0]
			up_bitrates[i] = r
		# print the bit-rates after calculating
		print_up_bitrates()
		print "iters:", j, "sum:", sum(up_bitrates)
		update_multipliers()
		# calculate the value of the objective
		L_value = calculate_L()
		# store the value of this iteration
		L_h.append(L_value)
		print "The value of L:", L_value
		# if the value of the objective converges, stop the iteration
		if abs(L_value - pre_L) < 0.01:
			print "stop!!!!!!!!!!!!!!!"
			break
# calculate the value of the objective
def calculate_L():
	L = 0.0
	for i in range(n_uploader):
		temp = up_bitrates[i]
		L += math.log(viewers[i]*(math.log(1 + temp/r_min) - a) - k*c[i]*(temp - r_min)) - my_alpha[i]*(r_min - temp) - my_beta[i]*(temp - r_max) - my_gamma * temp
	L += my_gamma * r_whole
	return L

# update the multipliers
def update_multipliers():
	global ss, my_gamma
	print "pre-multipliers:", my_alpha, my_beta, my_gamma
	# update the step size
	ss_cur =  1.0 / ss
	ss += 1
	# update alpha 
	for i in range(n_uploader):
		my_alpha[i] = max(0, my_alpha[i] + ss_cur * (up_bitrates[i] - r_min)) 
	# update beta
	for i in range(n_uploader):
		my_beta[i] = max(0, my_beta[i] + ss_cur * (r_max - up_bitrates[i])) 
	#update gamma
	my_gamma = max(0, my_gamma + ss_cur * (r_whole - sum(up_bitrates)))

	print "post-multipliers:", my_alpha, my_beta, my_gamma
	
# print the bit-rate of each uploader
def print_up_bitrates():
	print "Here print the bit-rates of uploaders:"
	for i in range(n_uploader):
		print "uploader:",i, up_bitrates[i]

#solve_r1()
#solve_r2()
solve_r3()

#with open("L.csv", 'w') as f:
#	f.write(json.dumps(L_h) + "\n")

#print_up_bitrates()
