#!/usr/bin/python
# _*_ coding: utf-8 _*_

from naoqi import ALProxy
import vision_definitions
import numpy

class Nao:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.Connect()

    def Connect(self):
        try:
            self.Motion = ALProxy('ALMotion', self.ip, self.port)
            self.TextToSpeech = ALProxy('ALTextToSpeech', self.ip, self.port)
            #self.SpeechRecognition = ALProxy('ALSpeechRecognition', self.ip, self.port)
            self.RobotPosture = ALProxy("ALRobotPosture", self.ip, self.port)
            self.VideoDevice = ALProxy("ALVideoDevice", self.ip, self.port)
        except Exception, e:
            print e

    def Stiffness(self, mode):
        return self.Motion.post.stiffnessInterpolation("Body", mode, 0.1)

    def StartPosition(self):
        self.Stiffness(1)
        self.RobotPosture.goToPosture("Sit", 0.8)
        self.Stiffness(0)

    def GetImage(self):
        resolution = vision_definitions.kVGA
        colorSpace = vision_definitions.kBGRColorSpace
        fps = 30
        self.VideoDevice.unsubscribe("NaoVision")
        process = self.VideoDevice.subscribe("NaoVision", resolution, colorSpace, fps)
        nao_image = self.VideoDevice.getImageRemote(process)
        img = (numpy.reshape(numpy.frombuffer(nao_image[6], dtype = '%iuint8' % nao_image[2]), (nao_image[1], nao_image[0], nao_image[2])))
        return img

    def setSpeak(self, text):
        self.TextToSpeech.say(text)