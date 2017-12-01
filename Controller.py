import numpy as np
import cv2
from QtGUI import GUI
from Filters import Filter
import FourierTransform as FT

class Controller(object):

    def __init__(self):
        self.gui = GUI(self)
        self.filter = Filter((256,256))
        self.useFullContrastStretch = True
        self.openImage('YmW3f.png')
        self.gui.show()

    def setShape(self, s):
        # print("Controller.setShape")
        if s == 0:
            self.filter.setCircle(True)
        else:
            self.filter.setCircle(False)

        self.recomputeAndApplyMask()

    def setVariant(self, v):
        if v == 0:
            self.filter.setVariant(False)
        else:
            self.filter.setVariant(True)
        self.recomputeAndApplyMask()

    def setMaskFunction(self, m):
        masks = {}
        masks[0] = "ideal"
        masks[1] = "gaussian"
        masks[2] = "butterworth"
        self.filter.setMaskFunction(masks[m])
        self.recomputeAndApplyMask()

    def setFrequency(self, f):
        self.filter.setFrequency(f)
        self.recomputeAndApplyMask()

    def setFrequencySpan(self, p):
        self.filter.setFrequencySpan(p)
        self.recomputeAndApplyMask()

    def setAngle(self, a):
        self.filter.setAngle(a)
        self.recomputeAndApplyMask()

    def setAngleSpan(self, s):
        self.filter.setAngleSpan(s)
        self.recomputeAndApplyMask()

    def setOrder(self, o):
        self.filter.setOrder(o)
        self.recomputeAndApplyMask()

    def recomputeAndApplyMask(self):
        self.mask = self.filter.generateMask()
        result_ft = self.mask * self.ft
        self.result = np.abs(FT.inverse(result_ft)).astype(np.uint8)
        if self.useFullContrastStretch:
            self.gui.setResult(FT.normalize(self.result, False))
        self.gui.setResult(self.result)
        # self.gui.setMask(self.filter.maskImage)
        self.gui.setMask(FT.normalize(result_ft))

    def openImage(self, filename):
        np_image = cv2.imread(filename, 0)
        self.setImage(np_image)

    def setImage(self, np_image):
        self.image = np_image
        self.ft = FT.forward(self.image)
        self.filter.shape = self.image.shape
        self.recomputeAndApplyMask()
        self.gui.setImage(self.image)
        self.gui.setFT(FT.normalize(self.ft))

if __name__ == '__main__':
    Controller()
