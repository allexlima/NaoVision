#!/usr/bin/python
# _*_ coding: utf-8 _*_

from Nao import Nao
from Vision import Vision

if __name__ == "__main__":
    Robot = Nao('192.168.1.104', 9559)
    Detect = Vision(Robot)

    Robot.StartPosition()
    if Detect.identifyColor() == True:
        Robot.setFinish()