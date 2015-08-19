#!/usr/bin/python
# _*_ coding: utf-8 _*_

import cv2
import numpy

class Vision:
    def __init__(self, device):
        self.device = device
        self.todasCores = 0
        self.Df = 0
        self.cores = [
            ["Azul", numpy.array([100, 150, 30]), numpy.array([130, 255, 255]), False],
            ["Amarelo", numpy.array([15, 100, 80]), numpy.array([30, 255, 255]), False],
            ["Vermelho", numpy.array([0, 60, 55]), numpy.array([3, 255, 255]), False],
            ["Verde", numpy.array([50, 90, 30]), numpy.array([80, 255, 255]), False]
        ]

    def getColor(self):
        img = self.device.GetImage()
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        for i in range(0, len(self.cores), 1):
            self.todasCores += cv2.inRange(hsv, self.cores[i][1], self.cores[i][2])

        kernel = numpy.ones((20, 20), numpy.uint8)
        erode = cv2.erode(self.todasCores, kernel, iterations=1)
        dilate = cv2.dilate(erode, kernel, iterations=1)

        self.Df = erode

        _i, contours, _h = cv2.findContours(dilate, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

        for point in contours:
            x, y, w, h = cv2.boundingRect(point)
            cx, cy = x+w/2, y+h/2

            color = hsv.item(cx, cy, 0)
            identified = False

            for i in range(0, len(self.cores), 1):
                if color in range(self.cores[i][1][0], self.cores[i][2][0]+1):
                    self.device.setSpeak(self.cores[i][0])
                    identified = True
                    break

            if identified is not True:
                 self.device.setSpeak("Não conheço esta cor")

    def show(self):
        cv2.imshow("NAOVision RealCam", self.Df)
        cv2.waitKey(0)