#!/usr/bin/python
# _*_ coding: utf-8 _*_

import cv2
import numpy

camera = cv2.VideoCapture(1)
points = None

while cv2.waitKey(True) != 27:
    _r, imagem = camera.read()
    imagem = cv2.flip(imagem, 90)
    todasAsCores = 0

    hsv = cv2.cvtColor(imagem, cv2.COLOR_BGR2HSV)

    cores = [ # Cores das bolinhas
        # ["Color_name", hsv_min, hsv_max, BGR, identified (default False)]
        ["Azul", numpy.array([100, 150, 30]), numpy.array([130, 255, 255]), [255, 0, 0], False],
        ["Amarelo", numpy.array([15, 100, 60]), numpy.array([25, 255, 255]), [0, 255, 255], False],
        ["Vermelho", numpy.array([0, 60, 55]), numpy.array([5, 255, 255]), [0, 0, 255], False],
        ["Verde", numpy.array([50, 90, 30]), numpy.array([80, 255, 255]), [0, 255, 0], False]
    ]

    for i in range(0, len(cores), 1):
        todasAsCores += cv2.inRange(hsv, cores[i][1], cores[i][2])

    thresholding = cv2.adaptiveThreshold(todasAsCores, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

    #transformações morfológicas
    kernel = numpy.ones((20, 20), numpy.uint8)
    erode = cv2.erode(todasAsCores, kernel, iterations=1)
    dilate = cv2.dilate(erode, kernel, iterations=1)

    blur = cv2.blur(dilate, (7, 7))

    contours, _h = cv2.findContours(blur, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    font = cv2.FONT_HERSHEY_SIMPLEX

    if contours:
        for point in contours:
            x, y, w, h = cv2.boundingRect(point)
            cx, cy = x+w/2, y+h/2

            for i in range(0, len(cores), 1):
                if hsv.item(cy, cx, 0) in range(cores[i][1][0], cores[i][2][0]) and cores[i][4] == False:
                    cv2.rectangle(imagem, (x, y), (x+w, y+h), cores[i][3], 2)
                    ponto = cores[i][0] + ', P(' + str(cx) + ', ' + str(cy) + ')'
                    cv2.putText(imagem, ponto, (cx-(len(ponto)*2), cy), font, .4, (255, 255, 255))
                    cores[i][4] = True
                    print ponto
                    break

    cv2.imshow('NaoColors', imagem)

cv2.destroyAllWindows()