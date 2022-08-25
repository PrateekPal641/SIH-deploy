from email.mime import image
from tkinter import Image
from tkinter.tix import IMAGE
from django.shortcuts import redirect, render
import qrcode 
import PIL.Image
# from qrgenerator.models import qrc
import cv2
import uuid
no=6
def qr(request):
    global no
    data=""
    if request.method=="POST":
        no=no+1
        data=str(uuid.uuid4())
        img=qrcode.make(data)
        name: str = "test"+ str(no) +".png"
        img.save("static/qrcode/test.png")
        image_data: IMAGE = open("static/qrcode/test.png", "rb").read()
        # print(image_data)
        # qrc(serialn=name, qr_code = image_data).save()
    else:
        pass
    return render(request,"qr/index.html",{'data':data})



def video_reader(request):
    # print("HELLO WORLD")
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

    return redirect('/../qrgenerator/')

# print(video_reader())