import cv2
from cvzone.HandTrackingModule import HandDetector
from time import  sleep
from pynput.keyboard import Controller, Key

cap = cv2.VideoCapture(0)
cap.set(4, 720)
cap.set(3, 1280)

detector = HandDetector(detectionCon=0.8, maxHands=2)
keys = [["Q","W","E", "R", "T", "Y", "U", "I", "O","P"],
        ["A","S", "D", "F", "G", "H", "J", "K","L", ";"],
        ["Z","X", "C", "V", "B", "N", "M",",", ".", "/"]]
finalText = ""
keyboard = Controller()

def drawAll(img, buttonList):
    for button in buttonList:
        x, y = button.pos
        w, h = button.size
        cv2.rectangle(img, button.pos, (x + w, y + h), (50, 50, 50), cv2.FILLED)
        cv2.putText(img, button.text, (x + 20, y + 65), cv2.FONT_HERSHEY_PLAIN,
                    4, (255, 255, 255), 4)
    return img

class Button():
    def __init__(self, pos, text, size=[85, 85]):
        self.pos = pos
        self.size = size
        self.text = text
        x, y = self.pos
        w, h = self.size


buttonList = []
for i in range(3):
    for x, key in enumerate(keys[i]):
        buttonList.append(Button([100 + 100 * x + 50, 100 * i + 430], key))

while True:
    success, img = cap.read()
    hands, img = detector.findHands(img, flipType=False)
    img=drawAll(img, buttonList)

    if hands:

        for button in buttonList:
            x,y= button.pos
            w, h = button.size
            finger_pos = hands[0]["lmList"][8]
            if x < finger_pos[0] < x+w and y < finger_pos[1] < y+w :
                cv2.rectangle(img, button.pos, (x + w, y + h), (190, 190, 190), cv2.FILLED)
                cv2.putText(img, button.text, (x + 20, y + 65), cv2.FONT_HERSHEY_PLAIN,
                            4, (255, 255, 255), 4)

                l, _ = detector.findDistance(finger_pos[:-1], hands[0]["lmList"][12][:-1])


                if l<33:
                    cv2.rectangle(img, button.pos, (x + w, y + h), (255, 255, 255), cv2.FILLED)
                    cv2.putText(img, button.text, (x + 20, y + 65), cv2.FONT_HERSHEY_PLAIN,
                                4, (255, 255, 255), 4)
                    keyboard.press(button.text)
                    finalText+= button.text
                    if button.text == ".":
                        with keyboard.pressed(Key.cmd_l):
                            keyboard.press("3")
                    sleep(0.4)

    cv2.rectangle(img, (150, 300), (700, 400), (50, 50, 50), cv2.FILLED)
    cv2.putText(img, finalText, (160, 385), cv2.FONT_HERSHEY_PLAIN,
                5, (255, 255, 255), 5)
    cv2.imshow("Image", img)
    cv2.waitKey(1)