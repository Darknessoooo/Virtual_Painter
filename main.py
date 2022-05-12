from csv import list_dialects
from pkgutil import ImpImporter
import handtrackingmodule as htm
import cv2
import os

folderPath = "Header"
listHeader = os.listdir(folderPath)
print(listHeader)

cap = cv2.VideoCapture(0)
width = 1920
height = 1080
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
        cv2.imshow("window", image)
        if cv2.waitKey(1) &  0xFF == 27:  # esc
            break


