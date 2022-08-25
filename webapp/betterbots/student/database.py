import cv2
import deepface
from deepface import DeepFace
import os
import pandas as pd
import mysql.connector
from pathlib import Path
from models import studata


def video_reader():
    cam = cv2.VideoCapture(0,cv2.CAP_DSHOW)
    detector = cv2.QRCodeDetector()
    while True:
        _, img = cam.read()
        cv2.imshow("img", img)
        data, bbox, _ = detector.detectAndDecode(img)
        if data:
            print("QR Code detected-->", data)
            break
        if cv2.waitKey(1) == ord("q"):
            break
    cam.release()
    cv2.destroyAllWindows()
    cam = cv2.VideoCapture(0,cv2.CAP_DSHOW)
    while True:
        _, img = cam.read()
        cv2.imshow("img", img)
        if cv2.waitKey(1) == ord("s"):
            cv2.imwrite('image.jpg' ,img)
            # df = DeepFace.verify(img_path = "E:\SIH\SIH\SIH\webapp\image.jpg", db_path = "E:/SIH/SIH/SIH/webapp/betterbots/static/STUDENTS PAGE/images")
            # print(df)
            # obj = DeepFace.analyze(img_path = "image.jpg", actions = ['age', 'gender', 'race', 'emotion'])
            result = DeepFace.verify(img2_path=r'E:\SIH\SIH\SIH\webapp\image.jpg',img1_path=r'E:\SIH\SIH\SIH\webapp\betterbots\static\STUDENTS PAGE\images\WhatsApp_Image_2022-07-12_at_4.02.35_PM.jpeg')
            # print(obj)
            if result['verified']==True:
                print('matched')
                break
            else:
                print('NOT VERIFIED')
                break

        if cv2.waitKey(1) == ord("q"):
            break
    cam.release()
    cv2.destroyAllWindows()
    return data,i
video_reader()
