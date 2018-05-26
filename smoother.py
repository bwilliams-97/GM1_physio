# Function that smooths values of array to act as low pass filter
# Arguments: array (of length n), n

from scipy import signal
import numpy as np

def smooth(x, window_length, window):
	# Takes arguments of vector (array), window_length and window type (string)
	
	if x.ndim != 1:
		raise ValueError ("Input vector must have dimension 1")
	
	if x.size != window_length:
		raise ValueError ("Input vector must match window size")
		
	# Concatenation of array - not really sure what it's doing...
	s=np.r_[x[window_length-1:0:-1], x, x[-2:-window_length-1:-1]]
	
	w = eval('np.'+window+'('+str(window_length)+')')
	
	y=np.convolve(w/w.sum(), s, mode='valid')
	
	return y
	
		

	
