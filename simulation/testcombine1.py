import copy
import json
import csv

def combine(l, n):
	answers = []
	one = [0]*n
	
	def next_c(li = 0, ni = 0):
		if ni == n:
			answers.append(copy.copy(one))
			print one
			return
		for lj in xrange(li, len(l)):
			one[ni] = l[lj]
			next_c(lj + 1, ni + 1)
	next_c()
	return answers

x = [i for i in range(100)]
number = 50
com =  combine(x, number)
with open('combine_%s'%number, 'w') as f:
	f.write(json.dumps(com))

with open('combine_%s'%number, 'r') as f:
	com = f.read()
	com = json.loads(com)
	print type(com)
	print com
	print len(com)


