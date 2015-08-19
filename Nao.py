#!/usr/bin/python
# _*_ coding: utf-8 _*_

from naoqi import ALProxy
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
        self.RobotPosture.goToPosture("Sit", 0.5)


    def GetImage(self):
        process = self.VideoDevice.subscribe("NaoColors", 2, 11, 5)
        nao_image = self.VideoDevice.getImageRemote(process)
        return (numpy.reshape(numpy.frombuffer(nao_image[6], dtype = '%iuint8' % nao_image[2]), (nao_image[1], nao_image[0], nao_image[2])))

    def TurnOff(self):
        self.proxy[4].unsubscribe("NaoColors")