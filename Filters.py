# FilterFunction:
def IdealFilterFunction()
def GaussianFilterFunction
def ButterworthFilterFunction

# Abstract class
class Filter:

	def __init__():
		self.mask_image = None
		self.filter_func = None

	def generateMask():


class CircularFilter(Filter):

	def __init__():
		self.frequency = None


class RingFilter(Filter):

	def __init__():
		self.frequency = None

	def generateMask(self):
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


