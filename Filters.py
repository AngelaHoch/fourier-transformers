"""
To use functions from this class, create a Filter object with the following values:
	shape of the image, stored as a tuple
	**filter_func (either ideal, gaussian, or butterworth) as a string
	**cutoff as an int
	**theta as a float
	**thetaspan (how many degrees wide is the slice) as a float
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

	def __init__(self, shape, filter_func = "ideal", cutoff = 20, theta = 0, thetaspan = 180, inverse = False, circle = True, ringwidth = 5, order = 1):
		self.shape = shape 
		self.cutoff = cutoff
		self.inverse = inverse
		self.theta = theta 
		self.ringwidth = ringwidth
		self.thetaspan = thetaspan
		self.order = order
		self.circle = circle
		self.func = filter_func

		if self.func == "notch":
			pass
		elif circle:
			self.func = self.func + "_circle"
		else:
			self.func = self.func + "_band"

		self.filter = getattr(self, self.func, self.ideal_circle)

	def setFrequency(self, f):
		self.cutoff = f

	def setFrequencySpan(self, s):
		self.ringwidth = s

	def setVariant(self, v):
		self.inverse = v

	def setShape(self, s):
		self.shape = s

	def setCircle(self, c):
		# print("Filter.setCircle")
		self.circle = c
		self.setMaskFunction(self.func.split('_')[0])

	def setMaskFunction(self, f):
		if f == "notch":
			self.func = f
		elif self.circle:
			self.func = f + "_circle"
		else:
			self.func = f + "_band"
		self.filter = getattr(self, self.func, self.ideal_circle)

	def setOrder(self, o):
		self.order = o

	def setAngleSpan(self, p):
		self.thetaspan = p

	def setAngle(self, a):
		self.theta = a

	def generateMask(self):
		if self.inverse:
			filter_mask = 1.0 - self.filter()
		else:
			filter_mask = self.filter()
		directional_mask = self.directional()
		self.final_filter_mask = filter_mask * directional_mask
		#self.final_filter_mask = directional_mask
		self.maskImage = (255 * self.final_filter_mask).astype(np.uint8)

		if self.inverse:
			self.maskImage = 255 - self.maskImage
			return 1.0 - self.final_filter_mask
		else:
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
				if x == 0:
					mask[j][i] = 0
				else:
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

		theta = self.theta * math.pi / 180
		theta_axis = math.tan(theta)

		#these are cartesian
		c_x1 = self.order * math.cos(theta)
		c_y1 = self.order * math.sin(theta)
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
		mask = 1 - np.zeros(self.shape)

		#spans 180 and over involves the whole matrix
		if self.thetaspan >= 180:
			return mask

		theta = self.theta * math.pi/180

		for j in range(mask.shape[0]):
			for i in range(mask.shape[1]):
				#r = ((j-mask.shape[0]/2)**2 + (i-mask.shape[1]/2)**2)**0.5
				y = j - mask.shape[0]//2
				x = i - mask.shape[1]//2
				alpha = math.atan2(y, x)

				delta_theta = self.clampangle(alpha - theta)
				delta_theta2 = self.clampangle(alpha - theta - math.pi)

				delta_theta = 180.0/math.pi*math.fabs(delta_theta)
				delta_theta2 = 180.0/math.pi*math.fabs(delta_theta2)

				if delta_theta > self.thetaspan/2 and delta_theta2 > self.thetaspan/2:
					mask[j][i] = 0


		return mask

	def clampangle(self, delta):
		if delta > math.pi:
			delta = delta - (2.0*math.pi)
		if delta < -math.pi:
			delta = delta + (2.0*math.pi)
		return delta