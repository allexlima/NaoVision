#!/usr/bin/python
# _*_ coding: utf-8 _*_

from Nao import Nao
<<<<<<< HEAD
from Vision import Vision
from cv2 import waitKey
=======
from Vision import *
import time
>>>>>>> parent of 5705c27... Versão Final (Completo)

if __name__ == "__main__":
    Robot = Nao('192.168.1.148', 9559)
    Robot.StartPosition()
    Camera = Vision(Robot)
    #Camera.show()
    #Camera.getColor()
