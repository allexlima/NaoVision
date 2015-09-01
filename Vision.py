#!/usr/bin/python
# _*_ coding: utf-8 _*_

import cv2
import numpy


class Vision:
    def __init__(self, device):
        self.device = device
        self.key = cv2.waitKey(True)
        self.cores = [
            ["Azul", numpy.array([100, 150, 100]), numpy.array([120, 255, 255]), False],
            ["Amarelo", numpy.array([15, 100, 80]), numpy.array([30, 255, 255]), False],
            ["Vermelho", numpy.array([0, 60, 55]), numpy.array([3, 255, 255]), False],
            ["Verde", numpy.array([50, 90, 30]), numpy.array([80, 255, 255]), False]
        ]

    def _setDevice(self, device):
        return cv2.VideoCapture(device)

    def _getImage(self):
        return self.device.GetImage()

    def _getHsvColor(self):
        return cv2.cvtColor(self._getImage(), cv2.COLOR_BGR2HSV)

    def _getJustColor(self):
        counter = 0
        for i in range(0, len(self.cores)):
            counter = counter + cv2.inRange(self._getHsvColor(), self.cores[i][1], self.cores[i][2])
        return counter

    def _setFilters(self):
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (20, 20))
        blur = cv2.GaussianBlur(self._getJustColor(), (9, 9), 0)
        threshold = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
        erode = cv2.erode(threshold[1], kernel, iterations=1)
        dilate = cv2.dilate(erode, kernel, iterations=1)
        return dilate

    def identifyColor(self):
        self.device.setSpeak("Deixe-me dar uma olhadinha!")
        contours = cv2.findContours(self._setFilters(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

        for point in contours[1]:
            self.device.setSpeak("huuum")
            x, y, w, h = cv2.boundingRect(point)
            cx, cy = x+w/2, y+h/2

            for i in range(0, len(self.cores)):
                try:
                    if self._getHsvColor().item(cx, cy, 0) in range(self.cores[i][1][0], self.cores[i][2][0]+1) and self.cores[i][3] == False:
                        self.device.setSpeak("Aaáh! Esta cor é " + self.cores[i][0])
                        self.cores[i][3] = True
                        return True
                except Exception, e:
                    self.device.setSpeak("Desculpe, não conheço esta cor!")
                    print e
                    return False