# Uses matplotlib to plot live data of input streams

import matplotlib
matplotlib.use("TkAgg")
from matplotlib.pyplot import figure, title, ylabel, xlabel, plot, show

def data_plot(x, y, flex):
	figure()
	plot(x)
	plot(y)
	plot(flex)
	title(r"Knee data")
	ylabel("Amplitude")
	xlabel("Sample")
	show()
	
