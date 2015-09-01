#!/usr/bin/python
# _*_ coding: utf-8 _*_

from Nao import Nao
from Vision import *
import time

if __name__ == "__main__":
    Robot = Nao('192.168.1.148', 9559)
    Robot.StartPosition()
    Camera = Vision(Robot)
    #Camera.show()
    #Camera.getColor()