#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Frequency Filtering

This program provides tools to filter an image in the frequency domain.

Author: Maxwell Ciotti
Last edited: Nov 2017
"""

import sys
from PyQt5.QtWidgets import QWidget, QSlider, QLabel, QApplication, QDesktopWidget, QComboBox, QLineEdit, QHBoxLayout, QVBoxLayout, QGridLayout, QSpinBox, QGraphicsView, QGraphicsScene
from PyQt5.QtCore import Qt, QByteArray
from PyQt5.QtGui import QPixmap, QBrush, QColor
import numpy as np


def npimage_to_pixmap(np_image):
	"""
	Converts a Numpy array-backed image into a QPixmap suitable for drawing in
	widgets.
	"""

	height, width = np_image.shape
	pgm_data = "P2\n{} {}\n{}\n".format(width, height, 255)
	for row in range(height):
		for col in range(width):
			pgm_data += str(np_image[row, col]) + " "
		pgm_data += "\n"

	pixmap = QPixmap()
	ba = QByteArray()
	pixmap.loadFromData(ba.append(pgm_data), "PGM")
	return pixmap


class QSpinSlider(QWidget):
	"""
	Combines a QLabel, QSlider, and a QSpinBox into one control widget.
	"""

	def __init__(self, label, initialValue):
		super().__init__()

		self.layout = QHBoxLayout()

		self.label = QLabel()
		self.label.setText(label)

		self.slider = QSlider(Qt.Horizontal, self)
		# self.slider.setFocusPolicy(Qt.NoFocus)
		self.slider.setGeometry(0, 0, 100, 30)
		self.slider.valueChanged[int].connect(self.onSliderChange)

		self.spin = QSpinBox(self)
		self.spin.valueChanged[int].connect(self.onSpinChange)

		self.layout.addWidget(self.label)
		self.layout.addWidget(self.slider)
		self.layout.addWidget(self.spin)
		self.layout.setContentsMargins(0, 0, 0, 0)
		self.setLayout(self.layout)


	def onSliderChange(self, value):
		self.spin.setValue(value)


	def onSpinChange(self, value):
		self.slider.setValue(value)


class QImageGrid(QWidget):
	"""
	Combines four QPixmap widgets in a grid.
	"""

	def __init__(self):
		super().__init__()

		self.scene_nw = QGraphicsScene()
		self.scene_ne = QGraphicsScene()
		self.scene_sw = QGraphicsScene()
		self.scene_se = QGraphicsScene()

		# bg = QBrush(Qt.lightGray, Qt.Dense3Pattern)
		bg = QColor(32, 32, 32, 255)

		self.scene_nw.setBackgroundBrush(bg)
		self.scene_ne.setBackgroundBrush(bg)
		self.scene_sw.setBackgroundBrush(bg)
		self.scene_se.setBackgroundBrush(bg)

		self.setGeometry(0, 0, 512, 512)
		self.layout = QGridLayout()
		self.view_nw = QGraphicsView(self.scene_nw)
		self.view_ne = QGraphicsView(self.scene_ne)
		self.view_sw = QGraphicsView(self.scene_sw)
		self.view_se = QGraphicsView(self.scene_se)
		self.view_nw.setGeometry(0, 0, 256, 256)
		self.view_ne.setGeometry(0, 0, 256, 256)
		self.view_sw.setGeometry(0, 0, 256, 256)
		self.view_se.setGeometry(0, 0, 256, 256)
		self.layout.addWidget(self.view_nw, 0, 0)
		self.layout.addWidget(self.view_ne, 0, 1)
		self.layout.addWidget(self.view_sw, 1, 0)
		self.layout.addWidget(self.view_se, 1, 1)
		self.layout.setSpacing(2)
		self.layout.setContentsMargins(2, 2, 2, 2)
		self.setLayout(self.layout)

		pm_nw = QPixmap('5903.jpg')
		pm_ne = QPixmap('5903.jpg')
		pm_sw = QPixmap('5903.jpg')
		pm_se = QPixmap('5903.jpg')
		self.image_nw = self.scene_nw.addPixmap(pm_nw)
		self.image_ne = self.scene_ne.addPixmap(pm_ne)
		self.image_sw = self.scene_sw.addPixmap(pm_sw)
		self.image_se = self.scene_se.addPixmap(pm_se)

		# TODO: set scene rect based on image size
		# w = pm_nw.width()
		# h = pm_nw.height()
		# self.scene_nw.setSceneRect(0, 0, w, h)
		# self.scene_ne.setSceneRect(0, 0, w, h)
		# self.scene_sw.setSceneRect(0, 0, w, h)
		# self.scene_se.setSceneRect(0, 0, w, h)

	def setImage(self, np_image):
		pm = npimage_to_pixmap(np_image)
		self.image_nw.setPixmap(pm)
		h, w = np_image.shape
		self.scene_nw.setSceneRect(0, 0, w, h)
		# get fourier transform of np_image
		# update image_ne
		# apply mask
		# get inverse fourier transform of masked

	def setMask(self, np_mask):
		pm = npimage_to_pixmap(np_mask)
		h, w = np_mask.shape
		self.scene_sw.setSceneRect(0, 0, w, h)
		self.image_sw.setPixmap(pm)



class QControlPanel(QWidget):
	"""
	Combines all control items into a single widget.
	"""

	def __init__(self):
		super().__init__()

		self.setGeometry(0, 0, 256, 512)
		self.layout = QVBoxLayout()
		self.controls = {}
		self.controls['frequency'] = QSpinSlider("Frequency", 20)

		for key in self.controls:
			self.layout.addWidget(self.controls[key])

		self.layout.addStretch(1)

		self.layout.setContentsMargins(16, 16, 16, 16)
		self.setLayout(self.layout)


if __name__ == '__main__':

	app = QApplication(sys.argv)

	window = QWidget()
	layout = QHBoxLayout()
	image_grid = QImageGrid()
	control_panel = QControlPanel()

	layout.addWidget(image_grid)
	layout.addWidget(control_panel)
	layout.setContentsMargins(0, 0, 0, 0)

	window.setWindowTitle('Frequency Filter')
	# window.setGeometry(0, 0, 800, 512)
	window.setLayout(layout)
	window.show()

	mask = np.zeros((256,256), dtype=np.uint8)
	image_grid.setMask(mask)

	sys.exit(app.exec_())