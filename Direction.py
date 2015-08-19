#!/usr/bin/python
# _*_ coding: utf-8 _*_

import cv2
import numpy
import time

class Video:
    def __init__(self, device=0):
        self.camera = cv2.VideoCapture(device)
        self.width = self.camera.get(3)
        self.height = self.camera.get(4)

    def drawLines(self, imagem):
        width, height = int(self.width), int(self.height)
        center = width/2
        cv2.line(imagem, (center, 0), (center, height), [255, 0, 0], 1)
        cv2.line(imagem, (center - center/4, 0), (center - center/4, height), [0, 255, 0], 1)
        cv2.line(imagem, (center + center/4, 0), (center + center/4, height), [0, 255, 0], 1)

    def getColor(self, imagem, color):
        cores = [ # Cores das bolinhas
            # ["Color_name", hsv_min, hsv_max]
            ["Azul", numpy.array([100, 150, 30]), numpy.array([130, 255, 255])],
            ["Amarelo", numpy.array([15, 100, 80]), numpy.array([30, 255, 255])],
            ["Vermelho", numpy.array([0, 60, 55]), numpy.array([3, 255, 255])],
            ["Verde", numpy.array([50, 90, 30]), numpy.array([80, 255, 255])]
        ]
        hsv = cv2.cvtColor(imagem, cv2.COLOR_BGR2HSV)
        return cv2.inRange(hsv, cores[color][1], cores[color][2])

    def morphologicalTransformation(self, imagem):
        kernel = numpy.ones((20, 20), numpy.uint8)
        erode = cv2.erode(imagem, kernel, iterations=1)
        dilate = cv2.dilate(erode, kernel, iterations=1)
        return cv2.blur(dilate, (5, 5))

    def getCenter(self, imagem):
        _i, contours, _h = cv2.findContours(imagem, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        if contours:
            for point in contours:
                x, y, w, h = cv2.boundingRect(point)
                cx, cy = x+w/2, y+h/2
                return cx, cy
        else:
            return 0, 0

    def identify(self, points):
        x, y = points
        width, height = int(self.width), int(self.height)
        center = width/2

        centerArea = range(center - center/4, center + center/4)
        leftArea = range(0, center - center/4)
        rightArea = range(center + center/4, width)

        if x in centerArea:
            return 0
        elif x in leftArea:
            return -1
        elif x in rightArea:
            return 1

    def apply(self):
        t_end = time.time() + 1
        while time.time() < t_end:
            _r, imagem = self.camera.read()
            imagem = self.getColor(imagem, 1)
            self.drawLines(imagem)
            imagem = self.morphologicalTransformation(imagem)

        return self.getCenter(imagem)

    def show(self):
        while cv2.waitKey(1) != 27:
            _r, imagem = self.camera.read()
            self.drawLines(imagem)
            cx, cy = self.apply()
            cv2.line(imagem, (cx, cy), (cx, cy), [255, 255, 255], 20)
            print self.identify((cx, cy))
            cv2.imshow("Window", imagem)

a = Video(0)
print a.identify(a.apply())