import cv2
import mediapipe as mp
import time

class handDetector():
    def __init__(self, mode=False, maxHands=2, complexity=0, detectionCon=0.75, trackCon=0.75):
        self.mpHands = mp.solutions.hands  # хотим распознавать руки (hands)
        self.hands = self.mpHands.Hands(mode, maxHands, complexity, detectionCon, trackCon)
        self.mpDraw = mp.solutions.drawing_utils  # утилита для рисования
        self.fingertips = [4, 8, 12, 16, 20] # кончики пальцев
        self.handList = {}  # словарь координа ключевых точек на руке
        self.fingers = {}  # словарь поднятых и опущеных пальцев

    def findHands(self, img, draw=False):
        RGB_image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # BGR -> RGB
        RGB_image.flags.writeable = False
        self.result = self.hands.process(RGB_image)  # ищем руки
        RGB_image.flags.writeable = True
        if draw:
            if self.result.multi_hand_landmarks:
                for handLms in self.result.multi_hand_landmarks:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)
            
        return img
    
    def findPosition(self, img, handNumber=0, draw=False):
        self.handList[handNumber] = []  # Список координат пальцев в пикселях
        h, w, c = img.shape
        xmax, ymax = 0, 0
        xmin, ymin = w, h
        if self.result.multi_hand_landmarks:  # если найдены руки
            myHand = self.result.multi_hand_landmarks[handNumber]  # извлекаем список найденных рук
            for lm in myHand.landmark:
                # преобразование координат из MediaPipe в Пиксели
                cx, cy = int(lm.x * w), int(lm.y * h)
                self.handList[handNumber].append((cx, cy))
                if cx > xmax:
                    xmax = cx
                if cy > ymax:
                    ymax = cy
                if cx < xmin:
                    xmin = cx
                if cy < ymin:
                    ymin = cy
            if draw:
                offset = 20
                cv2.rectangle(img, (xmin-offset, ymin-offset), (xmax+offset, ymax+offset), (0, 255, 0), 2)

    def fingersUp(self, handNumber=0):
        if self.result.multi_hand_landmarks:
            if len(self.result.multi_hand_landmarks) > handNumber:
                side_tumb = "left" # с какой стороны находится большой палец
                if self.handList[handNumber][17][0] < self.handList[handNumber][5][0]:
                    side_tumb = "right"
                
                self.fingers[handNumber] = []
                if side_tumb == "left":
                    if self.handList[handNumber][self.fingertips[0]][0] < self.handList[handNumber][self.fingertips[0] - 2][0]:
                        self.fingers[handNumber].append(1)
                    else:
                        self.fingers[handNumber].append(0)
                else:
                    if self.handList[handNumber][self.fingertips[0]][0] > self.handList[handNumber][self.fingertips[0] - 2][0]:
                        self.fingers[handNumber].append(1)
                    else:
                        self.fingers[handNumber].append(0)
                
                for i in range(1, 5):
                    if self.handList[handNumber][self.fingertips[i]][1] < self.handList[handNumber][self.fingertips[i]-2][1]:
                        self.fingers[handNumber].append(1)
                    else:
                        self.fingers[handNumber].append(0)
                
                print(self.fingers[handNumber])

def main():
    cap = cv2.VideoCapture(0)
    detector = handDetector()
    while cap.isOpened():  # пока камера "работает"
        success, image = cap.read()  # полчаем кадр с web-камеры (True/False, image)
        if not success:  # если не удалось получить кадр
            print("Не удалось получить изображение с web-камеры")
            continue  # переход к ближайшему циклу (while)
        
        image = cv2.flip(image, 1)  # зеркальное отражение картинки
        image = detector.findHands(image, True)
        countHands = 0
        if detector.result.multi_hand_landmarks:
            countHands = len(detector.result.multi_hand_landmarks)
        for i in range(countHands):
            detector.findPosition(image, i, True)
            detector.fingersUp(i)
        cv2.imshow("Image", image)
        if cv2.waitKey(1) &  0xFF == 27:  # esc
            break

main()