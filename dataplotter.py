# Uses matplotlib to plot live data of input streams

import matplotlib
matplotlib.use("TkAgg")
from matplotlib.pyplot import *
import time

def data_plot(x, y, flex):
	figure()
	plot(x)
	plot(y)
	plot(flex)
	title(r"Knee data")
	ylabel("Amplitude")
	xlabel("Sample")
	legend(["x", "y", "flex"])
	show()
	
def gui_plot():
	tick_img = imread('tick.png')
	cross_img = imread('cross.png')
	gui = figure('Leg raise status', figsize=(15,15))
	ax = gui.add_subplot(111)
	ax.text(0.1,0.8, "Leg above ground")
	ax.text(0.1,0.6, "Leg straightened")
	ax.text(0.1,0.4, "Upper leg muscle contracted")
	ax.text(0.1,0.2, "Foot pointed inwards") 
	
	ax.axes.get_xaxis().set_visible(False)
	ax.axes.get_yaxis().set_visible(False)
	
	extent_1l = (0.7,0.8,0.75,0.85)
	extent_1r = (0.8,0.9,0.75,0.85)
	extent_2l = (0.7,0.8,0.55,0.65)
	extent_2r = (0.8,0.9,0.55,0.65)
	extent_3l = (0.7,0.8,0.35,0.45)
	extent_3r = (0.8,0.9,0.35,0.45)
	extent_4l = (0.7,0.8,0.15,0.25)
	extent_4r = [0.8,0.9,0.15,0.25]
	
	im1l = imshow(tick_img, extent=extent_1l)
	im1r = imshow(cross_img, extent=extent_1r)
	im2l = imshow(tick_img, extent=extent_2l)
	im2r = imshow(cross_img, extent=extent_2r)
	im3l = imshow(tick_img, extent=extent_3l)
	im3r = imshow(cross_img, extent=extent_3r)
	im4l = imshow(tick_img, extent=extent_4l)
	im4r = imshow(cross_img, extent=extent_4r)
	
	ylim((0,1))
	xlim((0,1))
	
	draw()
		
	return im1l, im1r, im2l, im2r, im3l, im3r, im4l, im4r

def toggle_images(ula_success,lla_success,ulm_success,llm_success, im1l, im1r, im2l, im2r, im3l, im3r, im4l, im4r):
	# Toggle visible state of each image
	if ula_success is True: # First row
		im1l.set_visible(True)
		im1r.set_visible(False)
	else:
		im1l.set_visible(False)
		im1r.set_visible(True)
		
	if lla_success is True: # Second row
		im2l.set_visible(True)
		im2r.set_visible(False)
	else:
		im2l.set_visible(False)
		im2r.set_visible(True)
		
	if ulm_success is True: # Third row
		im3l.set_visible(True)
		im3r.set_visible(False)
	else:
		im3l.set_visible(False)
		im3r.set_visible(True)
	
	if llm_success is True: # Fourth row
		im4l.set_visible(True)
		im4r.set_visible(False)
	else:
		im4l.set_visible(False)
		im4r.set_visible(True)
		
	pause(0.005)

draw()
