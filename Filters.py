"""
TODO:
-setters and getters
-update generateMask
-notch
-directional
"""
"""
Issues:
-Butterworth filters do not seem to be fanning out correctly
"""
"""
To use functions from this class, create a Filter object with the following values:
	shape of the image, stored as a tuple
	filter_func (either ideal, gaussian, or butterworth) as a string
	cutoff as an int
	theta as a float
	thetaspan (how many degrees wide is the slice) as a float
	**inverse as a boolean (low pass and band pass will be "False")
	**circle as a boolean (band filters will be "False")
	**ringwidth as an int
	**order as an int

	**optional, they have default values
"""

import numpy as np
import cv2

class Filter:

	def __init__(self, shape, filter_func, cutoff, theta, thetaspan, inverse = False, circle = True, ringwidth = 1, order = 1):
		self.shape = shape 
		self.cutoff = cutoff
		self.inverse = inverse
		self.theta = theta
		self.ringwidth = ringwidth
		self.thetaspan = thetaspan
		self.order = order

		if circle:
			filter_func = filter_func + "_circle"
		else:
			filter_func = filter_func + "_band"

		self.filter = getattr(self, filter_func)

	def generateMask(self):
		"""
		height, width = self.shape
		image = np.zeros(shape, dtype=np.uint8)
		cx, cy = width / 2, height / 2
		for y in range(height):
			for x in range(width):
				r, theta = to_polar(x - cx, y - cy)
				# image[y,x] = 255 * self.filter_func.evaluate(r, theta)
				# image[y,x] = 255 * gaussian(r-freq, freq_range/2)
				# image[y,x] = 255 * butterworth((r-freq)/(freq_range/2), 4)
				# image[y,x] = 255 * (ideal(r-freq, freq_range/2) - ideal(r-freq, -freq_range/2))
		self.mask_image = image
		"""
		filter_mask = self.filter()
		directional_mask = self.directional()

		self.final_filter_mask = 1 - (filter_mask * directional_mask)

		self.final_filter_mask = 255 * self.final_filter_mask
		cv2.imshow('this thing', self.final_filter_mask)
		cv2.waitKey(0)
		cv2.destroyAllWindows()

		return self.final_filter_mask

	def ideal_circle(self):
		mask = np.zeros((self.shape[0],self.shape[1]))

		for j in range(mask.shape[0]):
			for i in range(mask.shape[1]):
				x = ((j-mask.shape[0]/2)**2 + (i-mask.shape[1]/2)**2)**0.5
				if x <= self.cutoff:
					mask[j][i] = 1

		if not self.inverse:
			mask = 1 - mask

		return mask

	def ideal_band(self):
		mask = np.zeros((self.shape[0],self.shape[1]))

		ring_min = self.cutoff - (self.ringwidth/2)
		ring_max = self.cutoff + (self.ringwidth/2)

		for j in range(mask.shape[0]):
			for i in range(mask.shape[1]):
				x = ((j-mask.shape[0]/2)**2 + (i-mask.shape[1]/2)**2)**0.5
				if x <= ring_max and x >= ring_min:
					mask[j][i] = 1

		if not self.inverse:
			mask = 1 - mask

		return mask

	def gaussian_circle(self):
		mask = np.zeros((self.shape[0],self.shape[1]))

		for j in range(mask.shape[0]):
			for i in range(mask.shape[1]):
				x = -((j-mask.shape[0]/2)**2 + (i-mask.shape[1]/2)**2)
				mask[j][i] = np.exp(x/((2*self.cutoff)**2))

		if not self.inverse:
			mask = 1 - mask

		return mask

	def gaussian_band(self):
		mask = np.zeros((self.shape[0],self.shape[1]))

		for j in range(mask.shape[0]):
			for i in range(mask.shape[1]):
				d = ((j-mask.shape[0]/2)**2 + (i-mask.shape[1]/2)**2)**0.5
				if d == 0:
					mask[j][i] = 0
					continue
				x = (((d**2)-(self.cutoff**2))/(d*self.ringwidth))
				mask[j][i] = np.exp(-(x**2))

		if not self.inverse:
			mask = 1 - mask

		return mask

	def butterworth_circle(self):
		mask = np.zeros((self.shape[0],self.shape[1]))

		for j in range(mask.shape[0]):
			for i in range(mask.shape[1]):
				x = ((j-(mask.shape[0]/2))**2 + (i-(mask.shape[1]/2))**2)**0.5
				mask[j][i] = 1/(1 + ((x/self.cutoff)**(2*self.order)))

		if not self.inverse:
			mask = 1 - mask

		return mask

	def butterworth_band(self):
		mask = np.zeros((self.shape[0],self.shape[1]))

		for j in range(mask.shape[0]):
			for i in range(mask.shape[1]):
				d = ((j-mask.shape[0]/2)**2 + (i-mask.shape[1]/2)**2)**0.5
				if d == self.cutoff:
					mask[j][i] = 1
					continue
				x = (d*self.ringwidth)/((d**2)-(self.cutoff**2))
				mask[j][i] = 1 - (1/(1 + (x**(2*self.order))))

		if not self.inverse:
			mask = 1 - mask

		return mask

	def notch(self):
		pass

	def directional(self):
		mask = np.zeros((self.shape[0],self.shape[1]))

		if not self.inverse:
			mask = 1 - mask
		return mask

newFilter = Filter((500,500), "butterworth", 100, 0, 0, circle = False, ringwidth = 4, order = 10)
newFilter.generateMask()