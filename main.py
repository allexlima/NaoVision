#!/usr/bin/python
# _*_ coding: utf-8 _*_

import cv2

from Nao import Nao

if __name__ == "__main__":
    Robot = Nao('127.0.0.1', 51393)
    Robot.StartPosition()