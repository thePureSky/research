#!/usr/bin/env python
# -*- coding:utf-8  -*-

import json
import matplotlib.pyplot as plt

with open("L.csv", "r") as f:
	line = f.readline()
	line = json.loads(line)
	print len(line), type(line),line[0]
	x = [i for i in range(len(line))]
	plt.plot(line, x)
	plt.savefig("plog.png", dpi=75)
	plt.show()
