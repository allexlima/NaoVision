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
            self.RobotPosture = ALProxy("ALRobotPosture", self.ip, self.port)
            self.VideoDevice = ALProxy("ALVideoDevice", self.ip, self.port)
            self.DCM = ALProxy("DCM", self.ip, self.port)
        except Exception, e:
            print e

    def Stiffness(self, mode):
        return self.Motion.post.stiffnessInterpolation("Body", mode, 0.1)

    def StartPosition(self):
        self.RobotPosture.goToPosture("Sit", 0.8)
        try:
            self.DCM.createAlias(["Movimentos", [
                "Device/SubDeviceList/RWristYaw/Position/Actuator/Value",
                "Device/SubDeviceList/RElbowYaw/Position/Actuator/Value",
                "Device/SubDeviceList/RShoulderPitch/Position/Actuator/Value",
                "Device/SubDeviceList/RElbowRoll/Position/Actuator/Value",
                "Device/SubDeviceList/RShoulderRoll/Position/Actuator/Value",
                "Device/SubDeviceList/HeadYaw/Position/Actuator/Value",
                "Device/SubDeviceList/HeadPitch/Position/Actuator/Value",
            ]])
            self.Motion.post.stiffnessInterpolation("Body", 0.8, 0.1)
            self.DCM.setAlias(["Movimentos", "Merge", "time-mixed", [
                [[1.05, self.DCM.getTime(800)]],
                [[1.91, self.DCM.getTime(800)]],
                [[0.31, self.DCM.getTime(500)]],
                [[0.085, self.DCM.getTime(800)]],
                [[0.16, self.DCM.getTime(100)]],
                [[-0.08, self.DCM.getTime(800)]],
                [[0.019, self.DCM.getTime(100)]]
            ]])
            time.sleep(0.5)
            self.DCM.set(["Device/SubDeviceList/RHand/Position/Actuator/Value", "Merge", [[0.6, self.DCM.getTime(1000)]]])
            self.setSpeak("Me dê uma bolinha, por favor!")
            time.sleep(1)
            self.DCM.set(["Device/SubDeviceList/RHand/Position/Actuator/Value", "Merge", [[0.4, self.DCM.getTime(500)]]])
            time.sleep(0.5)
            self.DCM.setAlias(["Movimentos", "Merge", "time-mixed", [
                [[0.99, self.DCM.getTime(800)]],
                [[1.07, self.DCM.getTime(800)]],
                [[0.6, self.DCM.getTime(500)]],
                [[1.43, self.DCM.getTime(800)]],
                [[-0.303, self.DCM.getTime(800)]],
                [[-0.43, self.DCM.getTime(800)]],
                [[0.45, self.DCM.getTime(100)]]
            ]])
        except Exception, e:
            print e

    def setFinish(self):
        time.sleep(1)
        try:
            self.DCM.setAlias(["Movimentos", "Merge", "time-mixed", [
                [[1.05, self.DCM.getTime(800)]],
                [[1.91, self.DCM.getTime(800)]],
                [[0.31, self.DCM.getTime(500)]],
                [[0.085, self.DCM.getTime(800)]],
                [[0.16, self.DCM.getTime(100)]],
                [[-0.08, self.DCM.getTime(800)]],
                [[0.019, self.DCM.getTime(100)]]
            ]])
            self.setSpeak("Prontinho!")
            self.DCM.set(["Device/SubDeviceList/RHand/Position/Actuator/Value", "Merge", [[0.6, self.DCM.getTime(1000)]]])
            time.sleep(1.5)
            self.Stiffness(0.0)
            self.RobotPosture.goToPosture("Sit", 0.8)
            self.Stiffness(0.0)
        except Exception, e:
            print e

    def GetImage(self):
        resolution = vision_definitions.kVGA
        colorSpace = vision_definitions.kBGRColorSpace
        fps = 30
        try:
            process = self.VideoDevice.subscribe("NaoVision", resolution, colorSpace, fps)
        except Exception, e:
            self.VideoDevice.unsubscribe("NaoVision")
            process = self.VideoDevice.subscribe("NaoVision", resolution, colorSpace, fps)

        nao_image = self.VideoDevice.getImageRemote(process)
        img = (numpy.reshape(numpy.frombuffer(nao_image[6], dtype = '%iuint8' % nao_image[2]), (nao_image[1], nao_image[0], nao_image[2])))
        return img

    def setSpeak(self, text):
        self.TextToSpeech.say(text)