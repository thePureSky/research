#! /usr/bin/env python
# -*- coding:utf-8  -*-

import os, sys
import random

# Initialization of configurations
# Number of servers
m = 1000

# Number of users
n = 1000

# Total size of the file
F = 1000.0

# the amount of segments
w = 2

# size of each segment
f_w = float(F) / w

# the value of l
l = 1

# the percentage each server store
x = float(l) / w

# samples of uploading rate
sample_rates = [1, 0.1]
len_samples = len(sample_rates)


# float operation error
float_error = 0.000001

# the max request number for each user, for coding scenario
request_number = 100

# the number of request for each user each segment, for without-coding scenario
segment_request_number = 10


# Initialization of the uploading rate of the servers with 0
r = [0 for i in range(m)]

def init_uploading_rate():
	for i in range(500):
	    r[i] = 1.0 
	for i in range(500, 1000):
	    r[i] = 0.1

def dynamic_init_rate():
	for i in range(m):
		random_number = random.random()
		if random_number > 0.5:
			r[i] = 1.0
		else:
			r[i] = 0.1
	r.sort()
	r.reverse()

# for coding, allocate the servers to the users randomly
def random_allocate_server(u):
	len_servers = len(u)
	max_number = min(request_number, len_servers)
	allocate_servers = []
	if len_servers == max_number:
		allocate_servers = u
	else:
		count = 0
		list_ran = []
		len_false = [True for i in range(len_servers)]
		while (True):
			random_number = random.randint(0, len_servers - 1)
			if len_false[random_number] == True:
				list_ran.append(random_number)
				count += 1
				len_false[random_number] = False
				if count == max_number:
					break

		for i in range(max_number):
			allocate_servers.append(u[list_ran[i]])

		
	#print allocate_servers
	return allocate_servers


# the size of the file is : F;
# each server store : x * F;
def simulation_with_coding():
	# the size each user can obtain from one server
	max_size = x * F

	# store the file already got from all servers for each user
	users_got_file = [0 for i in range(n)]
	users_leave = [False for i in range(n)]

	# count the number this server already served
	servers_served_count = [0 for i in range(m)]

	# for each user, store the file got from each server
	user_detail = []
	for i in range(n):
		temp = [0 for i in range(m)]
		user_detail.append(temp)
	
	# for each user, store the servers can be requested
	user_server_request = []
	for i in range(n):
		temp = [i for i in range(m)]
		user_server_request.append(temp)

	time = 0

	# store the number of users already got his file
	user_success_count = 0

	while (True):
		time += 1
		
		# store the request for each server
		request = []
		for i in range(m):
			temp = []
			request.append(temp)
		
		# the strategy to allocate the servers to each user
		for i in range(n):
			if users_leave[i] == True:
				continue
			temp = random_allocate_server(user_server_request[i])
			for t in temp:
				request[t].append(i)

		# tranfer data
		for i in range(m):
			if request[i] == []:
				continue

			number_request = len(request[i])
			each_user_can_obtain = r[i] / float(number_request)

			# update the size the users can obtain
			for j in request[i]:
				if users_leave[j] == True:
					continue
				gap = max_size - user_detail[j][i]
				if abs(gap) < float_error:
					continue
				if (gap - each_user_can_obtain) > float_error:
					user_detail[j][i] += each_user_can_obtain
					users_got_file[j] += each_user_can_obtain
				else:
					users_got_file[j] += gap
					user_detail[j][i] = max_size
					user_server_request[j].remove(i)
					servers_served_count[i] += 1
					#if servers_served_count[i] == n:
					#	print "Server", i, "leaved!"

				if users_got_file[j] >= F:
					user_success_count += 1
					users_leave[j] = True
					#print "User", j, "leaved!"
					#print "Success_count:", user_success_count
					
		
		if (user_success_count == n):
			break

#		print "time slot:", time

	#print users_got_file
	return time

def random_allocate_segments():
	s_temp = []
	for i in range(m):
		temp = set()
		#temp = []
		s_temp.append(temp)

	server_count = [0 for i in range(m)]

	replicate_number = int(m * l / w)
	#print replicate_number

	surplus_number = m * l - replicate_number * w

	segment_servers_number = [0] * w

	for i in range(w):
		if surplus_number != 0:
			segment_servers_number[i] = replicate_number + 1
			surplus_number -= 1
		else:
			segment_servers_number[i] = replicate_number
	
	#print segment_servers_number
	#print sum(segment_servers_number)


	layer_count = 0
	flag = 0
	for i in range(w):
		for j in range(segment_servers_number[i]):
			while(True):
				random_number = random.randint(0, m - 1)
				if i in s_temp[random_number]:
					continue
				if ((server_count[random_number] <= layer_count) and (len(s_temp[random_number]) < l)) :
					#s_temp[random_number].append(i)
					s_temp[random_number].add(i)
					server_count[random_number] += 1
					break
				#print i,j
			if flag + j + 1 == m:
				layer_count += 1
		flag += segment_servers_number[i]
		flag %= m

	print "initialization of the alocation of the segments: Done!"

	for i in range(len(s_temp)):
		if len(s_temp[i]) != l:
			print "ERROR! allocate error!"
			sys.exit(-1)

	for i in range(m):
		s_temp[i] = list(s_temp[i])


	return s_temp 

# the strategy to allocate the servers to each user, each segment
def random_allocate_server_for_this_segment(max_segment_request, u):
	len_servers = len(u)
	max_number = max_segment_request
	allocate_servers = []
	if len_servers == max_number:
		allocate_servers = u
	else:
		count = 0
		list_ran = []
		len_false = [True for i in range(len_servers)]
		while (True):
			random_number = random.randint(0, len_servers - 1)
			if len_false[random_number] == True:
				list_ran.append(random_number)
				len_false[random_number] = False
				count += 1
				if count == max_number:
					break

		for i in range(max_number):
			allocate_servers.append(u[list_ran[i]])
		
#	print allocate_servers
	return allocate_servers
	


# the size of the file is : f_w = F / w
def simulation_without_coding():
	# randomly allocate the segments to each server, each server store l segments
	servers_segments = random_allocate_segments()
	#print servers_segments

	# store whether the user leave
	users_leave = [False for i in range(n)]

	# for each user, store the size of the segments
	user_detail = []
	for i in range(n):
		temp = [0 for j in range(w)]
		user_detail.append(temp)
	
	# for each user, store whether the segment is received
	user_got_segments = []
	for i in range(n):
		temp = [False for j in range(w)]
		user_got_segments.append(temp)
	
	# for each segment, store its related servers
	segment_servers = []
	for i in range(w):
		temp = []
		segment_servers.append(temp)

	for i in range(len(servers_segments)):
		for j in servers_segments[i]:
			segment_servers[j].append(i)
	
	# the size of each segment
	size_segment = F / w

	time = 0

	user_success_count = 0
	user_success_segment = [0 for i in range(n)]

	
	# calculate the max request each segment can send
	replicate_number = int(m * l / w)
	max_segment_request = min(replicate_number, segment_request_number)

	while (True):
		time += 1
		
		request = []
		
		# for each server, initialize the request with 0
		for i in range(m):
			temp = []
			for j in range(w):
				temp.append([])
				
			request.append(temp)

		# the strategy to allocate the servers to each user, each segment
		for i in range(n):
			if users_leave[i] == True:
				continue
			for j in range(w):
				if user_got_segments[i][j] == True:
					continue
				temp = random_allocate_server_for_this_segment(max_segment_request, segment_servers[j])
				for t in temp:
					request[t][j].append(i)

		# transfer data
		for i in range(m):
			# count the request of different kind of segments for this server
			number_request_server = 0
			for j in range(w):
				if request[i][j] != []:
					number_request_server += 1
			if number_request_server == 0:
				continue

			rate_each_segment = r[i] / float(number_request_server)
			
			# update each user each segment
			for j in range(w):
				if request[i][j] != []:
					number_segment_users = len(request[i][j])
					rate_each_user = rate_each_segment / float(number_segment_users)
					
					# update the segment obtained by each user, each segment
					for k in request[i][j]:
						if user_got_segments[k][j] == True:
							continue
						gap = size_segment - user_detail[k][j]
						if (gap - rate_each_user) > float_error:
							user_detail[k][j] += rate_each_user
						else:
							user_detail[k][j] = size_segment
							user_got_segments[k][j] = True
							user_success_segment[k] += 1
							if user_success_segment[k] == w:
								user_success_count += 1
								users_leave[k] = True
								#print "User", k, "leaved!"

		if user_success_count == n:
			break

#		print "Time slot:" , time

	return time


def cal_avg_time_coding_static():
	# static network, one file
	init_uploading_rate()
	s_avg_time = simulation_with_coding()
	print "Considering the scenario in static network with coding, the average time is:", s_avg_time

def cal_avg_time_coding_dynamic():
	# dynamic network
	times = 100
	history = []
	for i in range(times):
		dynamic_init_rate()
		d_avg_time = simulation_with_coding()
		#if i % 100 == 1:
		#	print i, d_avg_time, float(sum(history)) / len(history)
		history.append(d_avg_time)
		print "times", i, d_avg_time
		print "average:", float(sum(history))/len(history)
	#print history
	print "Considering the scenario in dynamic network with coding, the average time is:", float(sum(history)) / times

def cal_avg_time_without_coding_static():
	# static network, one file
	init_uploading_rate()
	s_n_avg_time = simulation_without_coding()
	print "Considering the scenario in static network without coding, the average time (the random case) is:", s_n_avg_time

def cal_avg_time_without_coding_dynamic():
	# dynamic network
	times = 100
	history = []
	for i in range(times):
		dynamic_init_rate()
		d_n_avg_time = simulation_without_coding()

		history.append(d_n_avg_time)
		print "times:", i, d_n_avg_time
		print "average:", float(sum(history))/len(history)
	print "Considering the scenario in dynamic network without coding, the average time (the random case) is:", float(sum(history)) / times



# The main test code

# The scenario without coding, static network
#cal_avg_time_without_coding_static()

# The scenario without coding, dynamic network
#cal_avg_time_without_coding_dynamic()

# The scenario with coding, static network
#cal_avg_time_coding_static()

# The scenario with coding, dynamic network
cal_avg_time_coding_dynamic()
