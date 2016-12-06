#! /usr/bin/env python
# -*- coding:utf-8  -*-

# Configuration of sending rules:
# each packet: 0.1Mb
# for 1Mbps: 10 packets each second
# for 0.1Mbps: 1 packets each second
# Assume that for each server, it would not change its target to send

import json
import os, sys

# Initialization of configurations
# Number of servers
m = 1000

# Number of users
n = 1000

# Total size of the file
F = 1000.0

# the amount of segments
w = 10

# size of each segment
f_w = float(F) / w

# the value of l
l = 1

# the percentage each server store
x = float(l) / w

# samples of uploading rate
sample_rates = [1, 0.1]
len_samples = len(sample_rates)

# size of each packet
packet_size = 0.1

# float operation error
float_error = 0.00001

# Initialization of the uploading rate of the servers with 0
r = [0 for i in range(m)]

def init_uploading_rate():
	for i in range(500):
	    r[i] = 1.0
	for i in range(500, 1000):
	    r[i] = 0.1
	

def check(record):
	for i in record:
		if i == False:
			return True
	return False

def re_assign_for_one_server(assign_number, record, n):
	len_record = len(record)
	for i in range(len_record):
		index = int(i + n + m / w) % len_record
		if record[index] == False:
			assign_number[n] = index
			return True
	print "All of the users is ok!"
	return False

def	re_assign_for_all_servers(assign_number, record):
	if check(record) == False:
		return
	cur_number = 0
	len_record = len(record)
	for i in range(len(assign_number)):
		if record[cur_number] != True:
			assign_number = cur_number
		else:
			while(True):
				cur_number = (cur_number + 1) % len_record
				if record[cur_number] != True:
					assign_number = cur_number
					break
		cur_number = (cur_number + 1) % len_record

# the size of the file is : F
def simulation_with_coding():
	# calculate the amount of packets each server can send in each second.
	packets = [r[i] / packet_size for i in range(m)]
	#print packets


	# initialize the size each user has received
	user_size = [0 for i in range(n)]
	# show_10_users(user_size)

	# the amount of servers included
	all_servers_number = m
	print "For each file in coding scenario, the overall number of servers:", all_servers_number
	
	# the uploading rate the these worst servers
	r_server = [r[i] for i in range(all_servers_number)]
	
	# assign the first connect between users and servers
	assign_number = [i for i in range(all_servers_number)]
	#print "assign number:", assign_number


	# record whether the user has received enough size of the file
	record = [False for i in range(n)]

	# the average time 
	time = 0

	# store the data
	#if os.path.exists("coding.csv"):
	#	os.remove("coding.csv")

	# each slot is 1 second
	# check whether all users leave, if not, return True and continut to simulate
	while (check(record)):
		time += 1	
		#print "Time slot is:", time
		#if time == 1818:
		#	print user_size

		# write out to a file
		#with open("coding.csv", "a") as f:
		#	f.write(json.dumps(user_size) + "\n")

		# transport the file for each server
		for i in range(len(r_server)):
			# if this server can continue to send a packet to this user
			if record[assign_number[i]] == True:
				if re_assign_for_one_server(assign_number, record, i) == False:
					break
			# send the file
			this_need = F - user_size[assign_number[i]]
			if (this_need  - r_server[i]) > float_error:
				user_size[assign_number[i]] += r_server[i]
			elif abs(this_need - r_server[i]) < float_error:
				user_size[assign_number[i]] = F
				record[assign_number[i]] = True
			else:
				user_size[assign_number[i]] = F
				record[assign_number[i]] = True
				rest_size = r_server[i] - (F - user_size[assign_number[i]])

				# assign the rest the size to following users
				count = 1
				while (True):
					next_user = (assign_number[i] + count) % len(user_size)
					next_need = F - user_size[next_user]
					if (rest_size - next_need) < -float_error:
						user_size[next_user] += rest_size
						break
					elif abs(rest_size - next_need) < float_error:
						user_size[next_user] = F
						record[next_user] = True
						break
					else:
						user_size[next_user] = F 
						record[next_user] = True
						rest_size = rest_size - next_need
					if check(record) == False:
						break
					count += 1

		# re-assign the user to servers
		re_assign_for_all_servers(assign_number, record)
		#if time == 1818:
		#	print user_size
	
	# write out the final result
	#with open("coding.csv", "a") as f:
	#	f.write(json.dumps(user_size) + "\n")

	return time

# the size of the file is : f_w = F / w
def simulation_without_coding():
	# calculate the amount of packets each server can send in each second.
	packets = [r[i] / packet_size for i in range(m)]
	#print packets


	# initialize the size each user has received
	user_size = [0 for i in range(n)]
	# show_10_users(user_size)

	# the amount of servers included
	worst_servers_number = m / w
	print "For each segment, the number of servers in worst case:", worst_servers_number
	
	# the uploading rate the these worst servers
	r_server = [r[m - worst_servers_number + i] for i in range(worst_servers_number)]
	
	# assign the first connect between users and servers
	assign_number = [i for i in range(worst_servers_number)]
	#print "assign number:", assign_number


	# store the data
	#if os.path.exists("no_coding.csv"):
	#	os.remove("no_coding.csv")

	# record whether the user has received enough size of the file
	record = [False for i in range(n)]

	# the average time 
	time = 0

	# each slot is 1 second
	# check whether all users leave, if not, return True and continut to simulate
	while (check(record)):
		# write out to a file
		#with open("no_coding.csv", "a") as f:
		#	f.write(json.dumps(user_size) + "\n")

		#print "Time slot is:", time
		time += 1	
		#if time == 10000:
		#	print user_size
		# transport the file for each server
		for i in range(len(r_server)):
			# if this server can continue to send a packet to this user
			if record[assign_number[i]] == True:
				if re_assign_for_one_server(assign_number, record, i) == False:
					break
			# send the file
			this_need = f_w - user_size[assign_number[i]]
			if (this_need  - r_server[i]) > float_error:
				user_size[assign_number[i]] += r_server[i]
			elif abs(this_need - r_server[i]) < float_error:
				user_size[assign_number[i]] = f_w
				record[assign_number[i]] = True
			else:
				user_size[assign_number[i]] = f_w
				record[assign_number[i]] = True
				rest_size = r_server[i] - (f_w - user_size[assign_number[i]])
				# assign the rest the size to following users

				count = 1
				while (True):
					next_user = (assign_number[i] + count) % len(user_size)
					next_need = f_w - user_size[next_user]
					if (rest_size - next_need) < -float_error:
						user_size[next_user] += rest_size
						break
					elif abs(rest_size - next_need) < float_error:
						user_size[next_user] = f_w
						record[next_user] = True
						break
					else:
						user_size[next_user] = f_w 
						record[next_user] = True
						rest_size = rest_size - next_need
					if check(record) == False:
						break
					count += 1

		# re-assign the user to servers
		re_assign_for_all_servers(assign_number, record)
		#if time == 10000:
		#	print user_size

	# write out the final result
	#with open("no_coding.csv", "a") as f:
	#	f.write(json.dumps(user_size) + "\n")
	return time


def cal_avg_time_coding():
	# static network, one file
	init_uploading_rate()
	s_avg_time = simulation_with_coding()
	print "Considering the scenario in static network with coding, the average time is:", s_avg_time

def cal_avg_time_without_coding():
	# static network, one file
	init_uploading_rate()
	s_n_avg_time = simulation_without_coding()
	print "Considering the scenario in static network without coding, the average time (the worst case) is:", s_n_avg_time

def show_10_users(a):
	print "\nthe size got of 10 users:"
	for i in range(10):
		print a[i],
	print "\n"


# The main test code

# The scenario without coding
cal_avg_time_without_coding()

# The scenario with coding
cal_avg_time_coding()





