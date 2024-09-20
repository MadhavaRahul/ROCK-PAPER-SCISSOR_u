import random
import cv2
import cvzone
from cvzone.HandTrackingModule import HandDetector
import time

# Capture the video
cap = cv2.VideoCapture(0)

cap.set(3, 640)
cap.set(4, 480)
detector = HandDetector(maxHands=1)  # use only one hand
timer = 0
stateRes = False
startGam = False
score = [0, 0]  # initial score [player, AI]
roundCount=0
MaxR=5

while True:
    imgbg = cv2.imread("Resrc/BG.png")  # Make sure this file exists
    success, img = cap.read()

    imgscale = cv2.resize(img, (0, 0), None, 0.875, 0.875)
    imgscale = imgscale[:, 80:480]

    # Hand detection
    hands, img = detector.findHands(imgscale)

    if startGam:
        if stateRes is False:
            timer = time.time()-initialTime
            # Fix cv2.putText parameters (syntax error fix)
            cv2.putText(imgbg, str(int(timer)), (605, 435), cv2.FONT_HERSHEY_PLAIN, 6, (255, 0, 255), 4)
            if timer > 3:
                stateRes = True
                timer = 0

                if hands:
                    playerMove = None
                    hand = hands[0]
                    fingers = detector.fingersUp(hand)

                    if fingers == [0, 0, 0, 0, 0]:
                        playerMove = 1  # rock
                    elif fingers == [1, 1, 1, 1, 1]:
                        playerMove = 2  # scissor
                    elif fingers == [0, 1, 1, 0, 0]:
                        playerMove = 3  # paper

                    # AI move
                    randomNo = random.randint(1, 3)
                    imgB = cv2.imread(f'Resrc/{randomNo}.png', cv2.IMREAD_UNCHANGED)
                    imgbg = cvzone.overlayPNG(imgbg, imgB)

                    # GAME RESULT
                    # Player's win condition
                    if (playerMove == 1 and randomNo == 3) or \
                    (playerMove == 2 and randomNo == 1) or \
                    (playerMove == 3 and randomNo == 2):
                        score[1] += 1  # Player wins
                    # AI's win condition
                    if (playerMove == 3 and randomNo == 1) or \
                    (playerMove == 2 and randomNo == 3) or \
                    (playerMove == 1 and randomNo == 2):
                        score[0] += 1  # AI wins
                    roundCount+=1

    # Display score and image on background
    imgbg[234:654, 795:1195] = imgscale
    if stateRes:
        imgbg = cvzone.overlayPNG(imgbg, imgB, (149, 310))
        cv2.putText(imgbg, str(score[0]), (410, 215), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 6)
        cv2.putText(imgbg, str(score[1]), (1112, 215), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 6)

    # Show the background image
    cv2.imshow("BG", imgbg)
    
    # Wait for user input+-
    key = cv2.waitKey(1)
    if key == ord('s'):
        startGam = True  # Fix: assignment instead of comparison
        initialTime = time.time()
        stateRes = False
    if key == ord('q'):
        break
    if roundCount>=MaxR:
        break

# Release the capture and close windows
cap.release()
cv2.destroyAllWindows()

# Declare the result
if score[0] > score[1]:
    print("AI WINS!!!")
elif score[1] > score[0]:
    print("PLAYER WINS!!!")
else:
    print("TIE!!!")
