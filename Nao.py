#!/usr/bin/python
# _*_ coding: utf-8 _*_

from naoqi import ALProxy
import vision_definitions
import numpy
import time

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
            self.DCM = ALProxy("DCM", self.ip, self.port)
        except Exception, e:
            print e

    def Stiffness(self, mode):
        return self.Motion.post.stiffnessInterpolation("Body", mode, 0.1)

    def StartPosition(self):
        self.Stiffness(1)
        self.RobotPosture.goToPosture("Sit", 0.8)
        '''
        self.DCM.createAlias(["Movimentos", [
        "Device/SubDeviceList/LElbowYaw/Position/Actuator/Value",
        "Device/SubDeviceList/LWristYaw/Position/Actuator/Value",
        "Device/SubDeviceList/HeadPitch/Position/Actuator/Value",
        "Device/SubDeviceList/HeadYaw/Position/Actuator/Value"
        ]])
        self.Stiffness(1)
        self.DCM.setAlias(["Movimentos", "Merge", "time-mixed", [
        [[-1.413, self.DCM.getTime(1500)]],
        [[-1.810, self.DCM.getTime(100)]],
        [[0.43, self.DCM.getTime(300)]],
        [[0.58, self.DCM.getTime(2000)]],
        ]])
        '''
        self.DCM.set(["Device/SubDeviceList/LWristYaw/Position/Actuator/Value", "ClearBefore", [[-1.810, self.DCM.getTime(1000)]]])
        self.DCM.set(["Device/SubDeviceList/LElbowYaw/Position/Actuator/Value", "Merge", [[-1.413, self.DCM.getTime(1500)]]])
        self.DCM.set(["Device/SubDeviceList/HeadPitch/Position/Actuator/Value", "Merge", [[0.43, self.DCM.getTime(300)]]])
        self.DCM.set(["Device/SubDeviceList/HeadYaw/Position/Actuator/Value", "Merge", [[0.58, self.DCM.getTime(2000)]]])
        self.DCM.set(["Device/SubDeviceList/LHand/Position/Actuator/Value", "Merge", [[0.6, self.DCM.getTime(1000)]]])
        time.sleep(1)
        self.setSpeak("\Pau=20\ por favor\Pau=20\, me \Pau=10\ dê \Pau=10\ a \Pau=10\ bolinha")
        time.sleep(2)
        self.DCM.set(["Device/SubDeviceList/LHand/Position/Actuator/Value", "ClearAll", [[0.4, self.DCM.getTime(500)]]])

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
