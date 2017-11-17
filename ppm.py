

def np_to_pgm(np_image):
	height, width = np_image.shape
	result = "P2\n{} {}\n{}\n".format(width, height, 255)
	for row in range(height):
		for col in range(width):
			result += str(np_image[row, col]) + " "
		result += "\n"


pixmap = QPixmap()
pixmap.loadFromData(pgm, "PGM")