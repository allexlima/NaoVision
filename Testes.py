import naoqi
import time

dcm = naoqi.ALProxy("DCM", "192.168.1.115", 9559)

'''
dcm.createAlias(["Movimentos", [
    "Device/SubDeviceList/LElbowYaw/Position/Actuator/Value",
    "Device/SubDeviceList/LWristYaw/Position/Actuator/Value",
    "Device/SubDeviceList/HeadPitch/Position/Actuator/Value",
    "Device/SubDeviceList/HeadYaw/Position/Actuator/Value"
]])

dcm.setAlias(["Movimentos", "Merge", "time-mixed", [
    [[-1.413, dcm.getTime(1500)]],
    [[-1.815, dcm.getTime(1000)]],
    [[0.43, dcm.getTime(1000)]],
    [[0.58, dcm.getTime(2000)]]
]])
'''

dcm.set(["Device/SubDeviceList/LElbowYaw/Position/Actuator/Value", "ClearAll", [[-1.413, dcm.getTime(1000)]]])
time.sleep(3)
dcm.set(["Device/SubDeviceList/LWristYaw/Position/Actuator/Value", "ClearAll", [[-1.815, dcm.getTime(1000)]]])
