#!/usr/bin/python
# _*_ coding: utf-8 _*_

from Nao import Nao
from Vision import *
import time

if __name__ == "__main__":
    Robot = Nao('192.168.1.101', 9559)
    '''Robot.StartPosition()
    time.sleep(1)
    Robot.Motion.openHand("LHand")
    time.sleep(1)
    Robot.Motion.closeHand("LHand")'''
    Camera = Vision(Robot)
    Camera.getColor()