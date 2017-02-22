#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Author: leaf
# Time: 2017-02-20

# Description:
# this program is used to process the dataset from dashInTwitch

import sys,os

with open("dataset-twitchtv.csv") as f:
	count = 1
	pre_s = None
	line = f.readline().strip()
	while (line != ''):
		segments = line.split(',')
		print segments
		if pre_s != None and segments[0] != pre_s:
			f1.close()
			count += 1
		print count
		with open("slot-%d.csv" % count, 'a') as f1:
			f1.write(line + "\n")
			
		line = f.readline().strip()
		pre_s = segments[0]
