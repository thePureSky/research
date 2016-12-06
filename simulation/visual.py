#!/usr/bin/env python
# -*- coding:utf-8  -*-

import json
import sys, os

import matplotlib.pyplot as plt
import numpy as np
from moviepy.video.io.bindings import mplfig_to_npimage
import moviepy.editor as mpy

all_lines = []

#with open("coding.csv", "r") as f:
#	all_lines = f.readlines()
#	print "The number of all lines:", len(all_lines)

with open("no_coding.csv", "r") as f:
	all_lines = f.readlines()
	print "The number of all lines:", len(all_lines)

my_lines = [json.loads(all_lines[i]) for i in range(len(all_lines))]
# DRAW A FIGURE WITH MATPLOTLIB

all_count = 0

duration = 20
print  plt.subplots(1,figsize=(5,3), facecolor='white')
fig_mpl, ax = plt.subplots(1,figsize=(5,3), facecolor='white')
#xx = np.linspace(-2,2,200) # the x vector
xx = np.linspace(1,1000, 1000) # the x vector
print len(xx)
print xx
zz = lambda d: np.sinc(xx**2)+np.sin(xx+d) # the (changing) z vector
ax.set_title("The value")
ax.set_ylim(0,100)
line, = ax.plot(xx, my_lines[0])
#print ax.plot(xx, zz(0), lw=3)
#print line
#print zz(0)

# ANIMATE WITH MOVIEPY (UPDATE THE CURVE FOR EACH t). MAKE A GIF.

def make_frame_mpl(t):
	global all_count
	#print all_count
	#print my_lines[all_count][999], my_lines[all_count][500], my_lines[all_count][0]
	#line.set_ydata( zz(2*np.pi*t/duration))  # <= Update the curve
	line.set_ydata(my_lines[all_count])  # <= Update the curve
	#cc = 1818
	cc = 10000

	if all_count  >= cc:
		all_count = cc
	else:
		all_count = (all_count + 10)
        if all_count  >= cc:
            all_count = cc
	return mplfig_to_npimage(fig_mpl) # RGB image of the figure

animation =mpy.VideoClip(make_frame_mpl, duration=duration)
animation.write_gif("no_coding.gif", fps=50)



	
