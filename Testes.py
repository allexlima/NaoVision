import cv2

cam = cv2.VideoCapture(0)

while cv2.waitKey(True) != 27:
    _, img = cam.read()
    cv2.imshow("oi", img)