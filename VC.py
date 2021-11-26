import math

import cv2
import time
import numpy as np
import Hmodule
import screen_brightness_control as sbc

from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume


get_camera = cv2.VideoCapture(0)

get_camera.set(3, 640)  # setting camera Width
get_camera.set(4, 480)  # setting camera height

get_hands = Hmodule.handDetector()

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
Loudness_availability = volume.GetVolumeRange()

minLoudness  = Loudness_availability[0]
maxLoudness = Loudness_availability[1]
ar = 0
while True:
    res, img = get_camera.read()
    new_img = get_hands.findHands(img)
    hand_lst, box = get_hands.findPosition(img, draw=True)
    if len(hand_lst) > 0:
        ar = ((box[2] - box[0]) * (box[3] - box[1])) // 100
        if 500 < ar < 1000:

            x1, y1 = hand_lst[4][1], hand_lst[4][2]
            x2, y2 = hand_lst[8][1], hand_lst[8][2]

            xb1, yb1 = hand_lst[4][1], hand_lst[4][2]
            xb2, yb2 = hand_lst[12][1], hand_lst[12][2]

            cv2.circle(img, (x1, y1), 15, (255, 255, 0), cv2.FILLED)
            cv2.circle(img, (x2, y2), 15, (255, 255, 0), cv2.FILLED)
            cv2.line(img, (x1, y1), (x2, y2), (255, 255, 0), 3)
            cv2.circle(img, ((x2 + x1) // 2, (y2 + y1) // 2), 15, (255, 0, 255), cv2.FILLED)
            metric = np.interp(math.hypot(x2 - x1, y2 - y1), [70, 200], [minLoudness, maxLoudness])
            m2 = np.interp(math.hypot(xb2 - xb1, yb2- yb1),[70, 200], [0, 100])
            sbc.set_brightness(m2)
            # print(m2)
            # print(metric)
            volume.SetMasterVolumeLevel(metric, None)

    # cv2.imshow("Image", img)
    cv2.waitKey(1)


