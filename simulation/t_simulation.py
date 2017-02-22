#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os,sys
from math import *
import operator
from scipy.stats import norm
#from sympy import integrate
from scipy import integrate

# the amount of servers
m = 1000
#m = 10
# the amount of users
n = 1000
#n = 10

# the size of a file
F = 1000

# segments of the file
w =  2

# the value of l
l = 1

# the percent of files
x = float(l) / w
#print x


# initialze the uploading rate of servers with 0
r = [0 for i in range(m)]

# initial the uploading rate of servers applying some strategies
# 500 with 1Mbps and 500 with 0.1 Mbps, with decreasing order
def init_uploading_rate():
	for i in range(500):
		r[i] = 1.0
	for i in range(500, 1000):
		r[i] = 0.1


def init_uploading_rate_2():
	for i in range(10):
		r[i] = 0.1 * (i+1)
		  #print r[0], r[1], r[99], r[100], r[101],r[199],r[200],r[201], r[999]
	r.sort()
	r.reverse()
	print r

def calculate_x_i(i):
	sum_1 = 0.0
	for j in range(i + 1, m + 1):
		sum_1 += r[j - 1]
	#print sum_1
	x_i = float(r[i - 1]) / (sum_1 + i * r[i - 1])
	return x_i


def calculate_t_coding():
	# find i
	i_pivot = -1
	x_i = 0.0
	for i in range(1, m):
		if i == 1:
			x_i = calculate_x_i(i)
			print x_i
			if x_i < x:
				i_pivot = 0
				break
		x_i_plus_1 = calculate_x_i(i + 1)
		if x_i_plus_1 < x <= x_i:
			print "i:", i
			i_pivot = i
			break
		if i == m - 1:
			i_pivot = m - 1
	# test the value of i_pivot
	if i_pivot != -1:
		print "The value of i_pivot:", i_pivot
	else:
		print "ERROR!Test the value of i_pivot!"
		return

	# calculate the average time Tc
	
	sum_2 = 0.0
	for j in range(i_pivot + 1, m + 1):
		sum_2 += r[j - 1]
	#print sum_2
	
	Tc = float(n) * F * (1 - i_pivot * x) / sum_2
	print "Theorectically, the average time with coding is:", Tc
			


def calculate_t_no_coding():
	# calculate the sum of rate
	sum_3 = 0.0
#	print m/w
	start_point = m - int(m*l/w) + 1
#	print start_point

	for i in range(start_point, m + 1):
		sum_3 += r[i - 1] / l
#	print sum_3
	Tn = float(n * F) / (w * sum_3)
	print "Theorectically, the average time without coding in the worst case is:", Tn

# calculate the combination
def c(n, k):
	 return  reduce(operator.mul, range(n - k + 1, n + 1)) /reduce(operator.mul, range(1, k +1))

def cal_dynamic_coding():
	temp_sum = 0.0
	for i in range(1, 1001):
		temp_sum = temp_sum + (pow(10, 6) / (0.9 * i + 100)) * c(1000, i) * pow(0.5, i) * pow(0.5, 1000 - i)
	print "Theroectically, the value of coding in dynamic network is:", temp_sum


def cal_dynamic_no_coding():
	def f(x):
		G = norm.cdf((w*x - 550) / (4.5*sqrt(10*w)))
		g = (sqrt(w)/(4.5*sqrt(10)))*norm.pdf((w*x - 550) / (4.5*sqrt(10*w)))
		return (pow(10, 6) / x) * g * pow(1 - G, w-1)
	temp_sum = integrate.quad(f, 0, 1000)

	print "Theroectically, the value of no-coding in dynamic network is:", temp_sum


init_uploading_rate()
#init_uploading_rate_2()

calculate_t_coding()
calculate_t_no_coding()
cal_dynamic_coding()
cal_dynamic_no_coding()


