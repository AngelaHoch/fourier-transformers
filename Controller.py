import numpy as np
import cv2

class Controller(object):

    def __init__(self, image):
        self.filter = Filter(image.shape)
        self.mask = self.filter.generateMask()
        GUI.setMask(self.Mask)

    def SetFrequency(self, f):
        self.filter.setFrequency(f)
        self.recomputeAndApplyMask()

    def SetVariant(self, v):
        self.filter.setVariant(v)
        self.recomputeAndApplyMask()

    def setShape(self, s):
        self.filter.setShape()
        self.recomputeAndApplyMask()

    def setMaskFunction(self, m):
        self.filter.setMaskFunction(m)
        self.recomputeAndApplyMask()

    def setOrder(self, o):
        self.filter.setOrder(o)
        self.recomputeAndApplyMask()

    def setSpan(self, p):
        self.filter.setSpan(p)
        self.recomputeAndApplyMask()

    def setAngle(self, a):
        self.filter.setAngle(a)
        self.recomputeAndApplyMask()

    def recomputeAndApplyMask(self):
        self.mask = self.filter.generateMask()
        self.applyMask()
        GUI.setMask(self.mask)

    def openImage(self, filename):
        np_image = cv2.open(filename, 0)
        self.setImage(np_image)

    def setImage(self, np_image):
        self.image = np_image
        self.ft = FT.forward(self.image)
        self.applyMask()
        GUI.setImage(self.image)
        GUI.setFT(self.ft)

    def applyMask(self):
        result_ft = self.mask * self.ft
        self.result = FT.inverse(result_ft)
        GUI.setResult(self.result)