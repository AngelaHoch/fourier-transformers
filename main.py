#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Frequency Filtering

This program provides tools to filter an image in the frequency domain.

Author: Maxwell Ciotti
Last edited: Nov 2017
"""

import sys
from PyQt5.QtWidgets import QWidget, QSlider, QLabel, QApplication, QDesktopWidget, QComboBox, QLineEdit, QHBoxLayout, QVBoxLayout, QGridLayout, QSpinBox, QGraphicsView
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap


class QSpinSlider(QWidget):

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


	# def onActivated(self, text):
	# 	self.label.setText(text)
	# 	self.label.adjustSize()


	def onSliderChange(self, value):
		self.spin.setValue(value)


	def onSpinChange(self, value):
		self.slider.setValue(value)


class QImageGrid(QWidget):
	def __init__(self):
		super().__init__()

		self.setGeometry(0, 0, 512, 512)
		self.layout = QGridLayout()
		self.image_nw = QGraphicsView()
		self.image_ne = QGraphicsView()
		self.image_sw = QGraphicsView()
		self.image_se = QGraphicsView()
		self.layout.addWidget(self.image_nw, 0, 0)
		self.layout.addWidget(self.image_ne, 0, 1)
		self.layout.addWidget(self.image_sw, 1, 0)
		self.layout.addWidget(self.image_se, 1, 1)
		self.layout.setSpacing(0)
		self.layout.setContentsMargins(0, 0, 0, 0)
		self.setLayout(self.layout)


class QControlPanel(QWidget):
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

	sys.exit(app.exec_())