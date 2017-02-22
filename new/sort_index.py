#!/usr/bin/env python
# -*- coding:utf-8 -*-

# Author: leaf
# Time: 2017-02-20

# Description:
# this program is used to process the dataset from dashInTwitch

import sys,os

listfile = os.listdir('./day-part')

for x in listfile:

	whole = []

	with open("./day-p/%s" % x, 'r') as f:
		line = f.readline().strip()
		while (line != ''):
			segments = line.split(',')
			segments[1] = int(segments[1])
			whole.append(segments)
			print segments
			line = f.readline().strip()

	whole = sorted(whole, key=lambda whole:whole[1])

		
	with open("./day-p/%s" % x, 'w') as f1:
		for i in range(len(whole)):
			whole[i][1] = str(whole[i][1])
			f1.write(','.join(whole[i]) + "\n")
