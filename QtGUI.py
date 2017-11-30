#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Frequency Filtering

This program provides tools to filter an image in the frequency domain.

Author: Maxwell Ciotti
Last edited: Nov 2017
"""

import sys
# from PyQt5.QtWidgets import QWidget, QSlider, QLabel, QApplication, QDesktopWidget, QComboBox, QLineEdit, QHBoxLayout, QVBoxLayout, QGridLayout, QSpinBox, QGraphicsView, QGraphicsScene, QButtonGroup
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QByteArray
from PyQt5.QtGui import QPixmap, QBrush, QColor, QImage
import numpy as np


def npimage_to_pixmap(np_image):
	"""
	Converts a Numpy array-backed image into a QPixmap suitable for drawing in
	widgets.
	"""

	w, h = np_image.shape
	data = np_image.reshape((1, w*h))
	return QPixmap.fromImage(QImage(data, w, h, QImage.Format_Grayscale8))


class QSpinSlider(QWidget):
	"""
	Combines a QLabel, QSlider, and a QSpinBox into one control widget.
	"""

	def __init__(self, label, initialValue, min, max):
		super().__init__()

		self.layout = QVBoxLayout()
		self.valueChanged = lambda value: None

		self.label = QLabel()
		self.label.setText(label)

		controls = QWidget()
		controls_layout = QHBoxLayout()
		controls_layout.setContentsMargins(0, 0, 0, 0)
		controls.setLayout(controls_layout)

		self.slider = QSlider(Qt.Horizontal, self)
		# self.slider.setFocusPolicy(Qt.NoFocus)
		self.slider.setGeometry(0, 0, 100, 30)
		self.slider.setMinimum(min)
		self.slider.setMaximum(max)
		self.slider.setValue(initialValue)
		self.slider.valueChanged[int].connect(self.onSliderChange)

		self.spin = QSpinBox(self)
		self.spin.setMinimum(min)
		self.spin.setMaximum(max)
		self.spin.setValue(initialValue)
		self.spin.valueChanged[int].connect(self.onSpinChange)

		self.layout.addWidget(self.label)
		controls_layout.addWidget(self.slider, stretch=1)
		controls_layout.addWidget(self.spin, stretch=0)
		self.layout.addWidget(controls)
		self.layout.setContentsMargins(0, 0, 0, 0)
		self.setLayout(self.layout)


	def connect(self, fn):
		self.valueChanged = fn


	def onSliderChange(self, value):
		self.spin.setValue(value)
		self.valueChanged(value)


	def onSpinChange(self, value):
		self.slider.setValue(value)
		self.valueChanged(value)


class QImageGrid(QWidget):
	"""
	Combines four QPixmap widgets in a grid.
	"""

	def __init__(self):
		super().__init__()

		self.setMinimumWidth(512)

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
		# self.set
		self.layout = QGridLayout()
		self.view_nw = QGraphicsView(self.scene_nw)
		self.view_ne = QGraphicsView(self.scene_ne)
		self.view_sw = QGraphicsView(self.scene_sw)
		self.view_se = QGraphicsView(self.scene_se)
		self.view_nw.setStyleSheet("QGraphicsView { border-style: none; }");
		self.view_ne.setStyleSheet("QGraphicsView { border-style: none; }");
		self.view_sw.setStyleSheet("QGraphicsView { border-style: none; }");
		self.view_se.setStyleSheet("QGraphicsView { border-style: none; }");
		self.view_nw.setGeometry(0, 0, 256, 256)
		self.view_ne.setGeometry(0, 0, 256, 256)
		self.view_sw.setGeometry(0, 0, 256, 256)
		self.view_se.setGeometry(0, 0, 256, 256)
		self.layout.addWidget(self.view_nw, 0, 0)
		self.layout.addWidget(self.view_ne, 0, 1)
		self.layout.addWidget(self.view_sw, 1, 0)
		self.layout.addWidget(self.view_se, 1, 1)
		self.layout.setSpacing(0)
		self.layout.setContentsMargins(0, 0, 0, 0)
		self.setLayout(self.layout)

		pm_nw = QPixmap('YmW3f.jpg')
		pm_ne = QPixmap('YmW3f.jpg')
		pm_sw = QPixmap('YmW3f.jpg')
		pm_se = QPixmap('YmW3f.jpg')
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

	def setNW(self, np_image):
		pm = npimage_to_pixmap(np_image)
		self.image_nw.setPixmap(pm)
		h, w = np_image.shape
		self.scene_nw.setSceneRect(0, 0, w, h)

	def setNE(self, np_image):
		pm = npimage_to_pixmap(np_image)
		self.image_ne.setPixmap(pm)
		h, w = np_image.shape
		self.scene_ne.setSceneRect(0, 0, w, h)

	def setSW(self, np_image):
		pm = npimage_to_pixmap(np_image)
		self.image_sw.setPixmap(pm)
		h, w = np_image.shape
		self.scene_sw.setSceneRect(0, 0, w, h)

	def setSE(self, np_image):
		pm = npimage_to_pixmap(np_image)
		self.image_se.setPixmap(pm)
		h, w = np_image.shape
		self.scene_se.setSceneRect(0, 0, w, h)



class QControlPanel(QWidget):
	"""
	Combines all control items into a single widget.
	"""

	def __init__(self):
		super().__init__()

		self.fn = {}
		self.fn['shapeChange'] = lambda id: id
		self.fn['variantChange'] = lambda id: id
		self.fn['functionChange'] = lambda id: id

		self.setGeometry(0, 0, 256, 512)
		# self.setSizePolicy(QSizePolicy.Fixed)
		self.setMinimumWidth(256)
		self.setMaximumWidth(256)
		self.layout = QVBoxLayout()
		self.controls = {}
		self.controls['frequency'] = QSpinSlider("Frequency", 20, 1, 256/2)
		self.controls['freq_span'] = QSpinSlider("Freq. span", 5, 1, 256/2)
		self.controls['theta'] = QSpinSlider("Theta", 0, 0, 180)
		self.controls['theta_span'] = QSpinSlider("Theta span", 180, 0, 180)
		self.controls['order'] = QSpinSlider("Order", 2, 1, 10)
		self.controls['order'].slider.setTickPosition(QSlider.TicksBelow)
		self.controls['order'].slider.setTickInterval(1)

		shape_group = QGroupBox("Filter Shape")
		shape_group_layout = QVBoxLayout()
		shape_group.setLayout(shape_group_layout)
		shape_button_circle = QRadioButton("Circle", shape_group)
		shape_button_band = QRadioButton("Band", shape_group)
		shape_group_layout.addWidget(shape_button_circle)
		shape_group_layout.addWidget(shape_button_band)
		self.layout.addWidget(shape_group)
		shape_button_group = QButtonGroup(shape_group)
		shape_button_group.addButton(shape_button_circle, 0)
		shape_button_group.addButton(shape_button_band, 1)
		shape_button_group.buttonClicked[int].connect(self.onShapeChange)

		variant_group = QGroupBox("Filter Variant")
		variant_group_layout = QVBoxLayout()
		variant_group.setLayout(variant_group_layout)
		variant_button_lowpass = QRadioButton("Low-pass", variant_group)
		variant_button_highpass = QRadioButton("High-pass", variant_group)
		variant_group_layout.addWidget(variant_button_lowpass)
		variant_group_layout.addWidget(variant_button_highpass)
		self.layout.addWidget(variant_group)
		variant_button_group = QButtonGroup(variant_group)
		variant_button_group.addButton(variant_button_lowpass, 0)
		variant_button_group.addButton(variant_button_highpass, 1)
		variant_button_group.buttonClicked[int].connect(self.onVariantChange)

		function_group = QGroupBox("Filter Function")
		function_group_layout = QVBoxLayout()
		function_group.setLayout(function_group_layout)
		function_button_ideal = QRadioButton("Ideal", function_group)
		function_button_gaussian = QRadioButton("Gaussian", function_group)
		function_button_butterworth = QRadioButton("Butterworth", function_group)
		function_group_layout.addWidget(function_button_ideal)
		function_group_layout.addWidget(function_button_gaussian)
		function_group_layout.addWidget(function_button_butterworth)
		self.layout.addWidget(function_group)
		function_button_group = QButtonGroup(function_group)
		function_button_group.addButton(function_button_ideal, 0)
		function_button_group.addButton(function_button_gaussian, 1)
		function_button_group.addButton(function_button_butterworth, 2)
		function_button_group.buttonClicked[int].connect(self.onFunctionChange)

		# self.layout.addWidget(QLabel("Filter Parameters"))
		self.layout.addWidget(self.controls['frequency'])
		self.layout.addWidget(self.controls['freq_span'])
		self.layout.addWidget(self.controls['theta'])
		self.layout.addWidget(self.controls['theta_span'])
		self.layout.addWidget(self.controls['order'])

		self.layout.addStretch(1)

		self.layout.setContentsMargins(16, 16, 16, 16)
		self.setLayout(self.layout)

	def onShapeChange(self, id):
		# print("GUI.onShapeChange")
		self.fn['shapeChange'](id)

	def onVariantChange(self, id):
		self.fn['variantChange'](id)

	def onFunctionChange(self, id):
		self.fn['functionChange'](id)

	def connect(self, param, fn):
		if param == 'shape':
			self.fn['shapeChange'] = fn
		elif param == 'variant':
			self.fn['variantChange'] = fn
		elif param == 'function':
			self.fn['functionChange'] = fn
		elif param in self.controls:
			self.controls[param].connect(fn)


class GUI:
	def __init__(self, controller):
		self.app = QApplication(sys.argv)

		self.window = QWidget()
		self.layout = QHBoxLayout()
		self.image_grid = QImageGrid()
		self.control_panel = QControlPanel()
		self.control_panel.connect('shape', controller.setShape)
		self.control_panel.connect('variant', controller.setVariant)
		self.control_panel.connect('function', controller.setMaskFunction)
		self.control_panel.connect('frequency', controller.setFrequency)
		self.control_panel.connect('freq_span', controller.setFrequencySpan)
		self.control_panel.connect('theta', controller.setAngle)
		self.control_panel.connect('theta_span', controller.setAngleSpan)
		self.control_panel.connect('order', controller.setOrder)

		self.layout.addWidget(self.image_grid)
		self.layout.addWidget(self.control_panel)
		self.layout.setContentsMargins(0, 0, 0, 0)

		self.window.setWindowTitle('Frequency Filter')
		# self.window.setGeometry(0, 0, 800, 512)
		self.window.setLayout(self.layout)
		self.window.show()

		# mask = np.zeros((256,256), dtype=np.uint8)
		# self.image_grid.setSW(mask)


	def show(self):
		sys.exit(self.app.exec_())

	def setFT(self, np_image):
		self.image_grid.setNE(np_image)

	def setImage(self, np_image):
		self.image_grid.setNW(np_image)

	def setMask(self, np_image):
		self.image_grid.setSW(np_image)

	def setResult(self, np_image):
		self.image_grid.setSE(np_image)

