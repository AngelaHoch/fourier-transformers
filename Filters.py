"""
TODO:
-setters and getters
"""
"""
Issues:
-Butterworth filters do not seem to be fanning out correctly
-theta = 45, thetaspan = 90, creates blank mask in directional: should create a >< shape. WHHHHHHHHHHHHHYYYYYYYYYYYYYY
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
import math

class Filter:

	def __init__(self, shape, filter_func, cutoff, theta, thetaspan, inverse = False, circle = True, ringwidth = 1, order = 1):
		self.shape = shape 
		self.cutoff = cutoff
		self.inverse = inverse
		self.theta = theta - 90
		self.ringwidth = ringwidth
		self.thetaspan = thetaspan
		self.order = order

		if filter_func == "notch":
			pass
		elif circle:
			filter_func = filter_func + "_circle"
		else:
			filter_func = filter_func + "_band"

		self.filter = getattr(self, filter_func, self.ideal_circle)

	def generateMask(self):
		filter_mask = self.filter()

		self.final_filter_mask = 255 * (1-filter_mask)
		cv2.imshow('inverse of filter', self.final_filter_mask)
		cv2.waitKey(0)
		cv2.destroyAllWindows()

		directional_mask = self.directional()

		self.final_filter_mask = 255 * (1-directional_mask)
		cv2.imshow('inverse of directional', self.final_filter_mask)
		cv2.waitKey(0)
		cv2.destroyAllWindows()

		#self.final_filter_mask = 1 - (filter_mask * directional_mask)
		self.final_filter_mask = (filter_mask * directional_mask)

		self.final_filter_mask = 255 * self.final_filter_mask
		cv2.imshow('final mask', self.final_filter_mask)
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

		if self.inverse:
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

		if self.inverse:
			mask = 1 - mask

		return mask

	def gaussian_circle(self):
		mask = np.zeros((self.shape[0],self.shape[1]))

		for j in range(mask.shape[0]):
			for i in range(mask.shape[1]):
				x = -((j-mask.shape[0]/2)**2 + (i-mask.shape[1]/2)**2)
				mask[j][i] = np.exp(x/((2*self.cutoff)**2))

		if self.inverse:
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

		if self.inverse:
			mask = 1 - mask

		return mask

	def butterworth_circle(self):
		mask = np.zeros((self.shape[0],self.shape[1]))

		for j in range(mask.shape[0]):
			for i in range(mask.shape[1]):
				x = ((j-(mask.shape[0]/2))**2 + (i-(mask.shape[1]/2))**2)**0.5
				mask[j][i] = 1/(1 + ((x/self.cutoff)**(2*self.order)))

		if self.inverse:
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

		if self.inverse:
			mask = 1 - mask

		return mask

	def notch(self):
		#currently using cuttoff to determine how large of an area is being covered
		#theta to determine the angle 
		#order to determine where along the the axis the center of the thingamabob is
		
		mask = np.zeros((self.shape[0],self.shape[1]))

		self.theta = self.theta * math.pi / 180
		theta_axis = math.tan(self.theta)

		#these are cartesian
		c_x1 = self.order / theta_axis
		c_y1 = self.order * theta_axis
		c_x2 = -1 * c_x1
		c_y2 = -1 * c_y1

		#cartesian to matrix:
		c_x1 = mask.shape[1]//2 + c_x1
		c_y1 = mask.shape[0]//2 + c_y1
		c_x2 = mask.shape[1]//2 + c_x2
		c_y2 = mask.shape[0]//2 + c_y2
		
		for j in range(mask.shape[0]):
			for i in range(mask.shape[1]):
				a = ((j-c_y1)**2 + (i-c_x1)**2)**0.5
				b = ((j-c_y2)**2 + (i-c_x2)**2)**0.5
				if a <= self.cutoff or b <= self.cutoff:
					mask[j][i] = 1

		if self.inverse:
			mask = 1 - mask

		return mask

	def directional(self):
		#matrix of all 1s
		mask = 1 - np.zeros((self.shape[0],self.shape[1]))

		#spans 180 and over involves the whole matrix
		if self.thetaspan >= 180:
			return mask

		self.theta = self.theta * math.pi / 180
		self.thetaspan = self.thetaspan * math.pi / 180

		#t1, t2 is the range of theta; the whole range spans 0 - 2pi radians. if t1 = t2, it is 2pi
		t1 = self.theta - (self.thetaspan)
		t2 = self.theta + (self.thetaspan)
		t1 = math.tan(t1)
		t2 = math.tan(t2)

		for j in range(mask.shape[0]):
			#matrix to cartesian
			cart_j = mask.shape[0]//2 - j
			
			if t1 == 0:
				i_1 = 0
			else:
				i_1 = cart_j/t1

			if t2 == 0:
				i_2 = mask.shape[1]
			else:
				i_2 = cart_j/t2

			#cartesian to matrix
			i_1 = mask.shape[1]//2 + i_1
			i_2 = mask.shape[1]//2 + i_2

			for i in range(mask.shape[1]):
				if i > i_1 and i < i_2:
					mask[j][i] = 0
				elif i < i_1 and i > i_2:
					mask[j][i] = 0

		return mask

#newFilter = Filter(//shape, //function, //cutoff, //theta, //theta span, //*inverse, //*circle, //*ringwidth, //*order)
newFilter = Filter((500,500), "notch", 5, 30, 180, ringwidth = 4, order = 20)
newFilter.generateMask()