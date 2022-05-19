
import handtrackingmodule as htm
import cv2
import os
import numpy as np


draw = False
erase = False
BRUSH_THICKNESS = 25
ERASE_THICKNESS = 100
draw_color = (0, 0, 0)
width = 1920
height = 1080
xp , yp = 0, 0
imgCanvas = np.zeros((height , width , 3), np.uint8)


folderPath = "Header"
header_list = []
listHeader = os.listdir(folderPath)

for imgPath in listHeader:
    image = cv2.imread(folderPath+'/'+imgPath)
    header_list.append(image)
header = header_list[-1]


cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
cv2.namedWindow("window", cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty("window", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)


while cap.isOpened():  # пока камера "работает"
        success, image = cap.read()  # полчаем кадр с web-камеры (True/False, image)
        if not success:  # если не удалось получить кадр
            print("Не удалось получить изображение с web-камеры")
            continue  # переход к ближайшему циклу (while)
        
        image = cv2.flip(image, 1)  # зеркальное отражение картинки


        detector = htm.handDetector()
        detector.findHands(image)
        detector.findFingersPosition(image)
        mhl = detector.result.multi_hand_landmarks
        h , w , c = header.shape
        if mhl:
            handCount = len(mhl)
            for i in range(handCount):
                x1 , y1 = detector.pointPosition[i][4][0], detector.pointPosition[i][4][1]
                x2 , y2 = detector.pointPosition[i][8][0], detector.pointPosition[i][8][1]
                cx , cy = (x1 + x2) // 2, (y1 + y2) // 2

                distance = detector.findDistance(4 , 8 , i)
                cv2.circle(image , (cx , cy), BRUSH_THICKNESS//2, draw_color, cv2.FILLED)
                if distance < 50:
                    if cy <= h:
                        if 10 <= cx <= 115:
                            header = header_list[0]
                            draw = True
                            erase = False
                            draw_color = (22 , 22 , 255)
                        elif 337 <= cx <= 420:
                            header = header_list[1]
                            draw = True
                            erase = False
                            draw_color = (255 , 0 , 0)
                        elif 550 <= cx <= 700:
                            header = header_list[2]
                            draw = True
                            erase = False
                            draw_color = (77 , 145 , 255)
                        elif 1405 <= cx <= 1574:
                            header = header_list[3]
                            draw = False
                            erase = True
                            draw_color = (0 , 0 , 0)
                            
                    cv2.circle(image , (cx , cy), BRUSH_THICKNESS, draw_color, cv2.FILLED)

                    if draw:
                        if xp == 0 and xp == 0:
                            xp, yp = cx, cy
                        cv2.line(image, (xp, yp), (cx, cy), draw_color, BRUSH_THICKNESS)
                        cv2.line(imgCanvas, (xp, yp), (cx, cy), draw_color, BRUSH_THICKNESS)

                    
                    if erase:
                        if xp == 0 and xp == 0:
                            xp, yp = cx, cy
                        cv2.line(image, (xp, yp), (cx, cy), draw_color, ERASE_THICKNESS)
                        cv2.line(imgCanvas, (xp, yp), (cx, cy), draw_color, ERASE_THICKNESS)

                xp , yp = cx, cy
        imgGray = cv2.cvtColor(imgCanvas, cv2.COLOR_BGR2GRAY)
        _, imgInv = cv2.threshold(imgGray , 10 , 255 , cv2.THRESH_BINARY_INV)
        imgInv = cv2.cvtColor(imgInv , cv2.COLOR_BAYER_BG2BGR)
        image = cv2.bitwise_and(image , imgInv)
        image = cv2.bitwise_or(image , imgCanvas)
        image[0:h, 0:w] = header
        cv2.imshow("window", image)
        if cv2.waitKey(1) &  0xFF == 27:  # esc
            break


