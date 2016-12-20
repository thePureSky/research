#!/usr/bin/env python
# -*- coding: utf-8 -*-

# the amount of servers
m = 1000
# the amount of users
n = 1000

# the size of a file
F = 1000

# segments of the file
w = 10

# the value of l
l = 9

# the percent of files
x = float(l) / w

#print x

# initialze the uploading rate of servers with 0
r = [0 for i in range(m)]

# initial the uploading rate of servers applying some strategies
# 500 with 1Mbps and 500 with 0.1 Mbps, with decreasing order
for i in range(500):
	r[i] = 1.0
for i in range(500, 1000):
	r[i] = 0.1

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
#			print x_i
			if x_i < x:
				i_pivot = 0
				break
		x_i_plus_1 = calculate_x_i(i + 1)
		if x_i_plus_1 < x <= x_i:
			print "i:", i
			i_pivot = i
			break
	# test the value of i_pivot
	if i_pivot != -1:
		print "The value of i_pivot:", i_pivot
	else:
		print "ERROR!Test the value of i_pivot!"
		return

	# calculate the average time Tc
	
	sum_2 = 0.0
	for j in range(i_pivot, m + 1):
		sum_2 += r[j - 1]
#	print sum_2
	
	Tc = float(n) * F * (1 - i_pivot * x) / sum_2
	print "Theorectically, the average time with coding is:", Tc
			


def calculate_t_no_coding():
	# calculate the sum of rate
	sum_3 = 0.0
#	print m/w
	start_point = 1000 - m/w + 1
#	print start_point

	for i in range(start_point, m + 1):
		sum_3 += r[i - 1]
#	print sum_3
	Tn = float(n * F) / (w * sum_3)
	print "Theorectically, the average time without coding in the worst case is:", Tn



calculate_t_coding()
calculate_t_no_coding()


