#!/usr/bin/python
# _*_ coding: utf-8 _*_
import naoqi
import time
tss = naoqi.ALProxy("ALTextToSpeech","192.168.0.1", 9559)
dcm = naoqi.ALProxy("DCM","192.168.0.1", 9559)

dcm.createAlias(["Movimentos", [
    "Device/SubDeviceList/LElbowYaw/Position/Actuator/Value",
    "Device/SubDeviceList/LWristYaw/Position/Actuator/Value",
    "Device/SubDeviceList/HeadPitch/Position/Actuator/Value",
    "Device/SubDeviceList/HeadYaw/Position/Actuator/Value"
   ]])

dcm.setAlias(["Movimentos", "Merge", "time-mixed", [
    [[-1.413, dcm.getTime(1500)]],
    [[-1.815, dcm.getTime(1000)]],
    [[0.43, dcm.getTime(600)]],
    [[0.58, dcm.getTime(2000)]],
]])

dcm.set(["Device/SubDeviceList/LHand/Position/Actuator/Value", "ClearAll", [[0.6, dcm.getTime(1000)]]])
time.sleep(1)
tss.say("\Pau=20\ por favor\Pau=20\, me \Pau=10\ dê \Pau=10\ a \Pau=10\ bolinha")
time.sleep(1)
dcm.set(["Device/SubDeviceList/LHand/Position/Actuator/Value", "ClearAll", [[0.4, dcm.getTime(500)]]])
