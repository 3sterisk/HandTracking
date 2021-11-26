import cv2
import mediapipe as mp

cap = cv2.VideoCapture(2)

initialize = mp.solutions.hands
hand = initialize.Hands()
mpDraw =  mp.solutions.drawing_utils

while True:
    res, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hand.process(imgRGB)
    # print(results.multi_hand_landmarks)


    if results.multi_hand_landmarks:
        for handlandmarks in results.multi_hand_landmarks:
            for id, lm in enumerate(handlandmarks.landmark):
                h, w, c  = img.shape
                cx, cy = int(lm.x*w), int(lm.y*h)
                print( id, cx, cy)
            mpDraw.draw_landmarks(img, handlandmarks, initialize.HAND_CONNECTIONS)







    cv2.imshow("Image", img)
    cv2.waitKey(1)
