from dataclasses import dataclass
from re import X
import re
# from socket import AI_DEFAULT
from xml.dom import ValidationErr
from django.http import HttpResponse
from django.shortcuts import redirect, render
from pytz import country_timezones
from django.utils.datastructures import MultiValueDictKeyError
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from django.contrib import messages
from student.models import studata
from django import forms
from math import ceil
from django.contrib.auth.decorators import login_required
from student.models import studata
import qrcode 
import PIL.Image
import cv2

dataid={}

def evlogin(request):
    if request.method=="POST":
        username: str =  request.POST['Center_ID']
        password =  request.POST['password']
        password = str(password) 
        print(username)
        print(password)
        
        user =None
        user = authenticate(username=username, password=password)
        if user is not None:
            print("yes")
            if user.is_evaluator==False:
                msg = 'UNAUTHORIZED'
                print(msg)
                messages.info(request,'UNAUTHORIZED')
                return redirect('/../evaluator/')
            login(request, user)
            return redirect('/../evaluator/scanqr')
        else:
            msg = 'User is not REGISTERED'
            print(msg)
            messages.info(request,'User is not REGISTERED ')
            return redirect('/../evaluator/') 
    return render(request, "EVALUATOR PAGE\login.html")

def attend(request):
    att = studata.objects.all()

    print(att)
    # n = len(att)
    # slides = n//4 + ceil((n/4) - (n//4))
    params = {'atten': att}
    return render(request, '''EVALUATOR PAGE\sttend.html''', params)

def scanqr(request):
    if request.user.is_authenticated:
        # print(request.user.image)
        return render(request, "EVALUATOR PAGE\scan.html")
    else:
        msg = 'Unauthorized'
        print(msg)
        messages.info(request,'UNAUTHORIZED!')
        return redirect('/../evaluator/')


def logev(request):
    logout(request)
    messages.info(request,'Successfully logged out!')
    return redirect('/../evaluator/')


def marks(request):
    print("HELLO WORLD")
    # is function ka kaam --> Qr aur face scan krke, student ke database se link krna qr code ko
    cam = cv2.VideoCapture(0,cv2.CAP_DSHOW)
    detector = cv2.QRCodeDetector()
    data=""
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
    if data=="":
        msg = 'INVALID QRCODE'
        print(msg)
        messages.info(request,'INVALID QRCODE')
        return redirect('/../evaluator/scanqr')
    try:
        posts=studata.objects.get(answerid=data)
        print(posts.marks)
        global dataid
        dataid['aid']=data;
        return redirect('/../evaluator/upload')
    except studata.DoesNotExist:
        msg = 'INVALID QRCODE'
        print(msg)
        messages.info(request,'INVALID QRCODE')
        return redirect('/../evaluator/scanqr')
    
def upload(request):
    if request.method=="POST":
        markso =  request.POST['markso']
        remarks =  request.POST['remarks']
        posts=studata.objects.get(answerid=dataid['aid'])
        posts.marks=markso
        posts.remarks=remarks
        posts.save()
        msg = 'MARKS UPDATED'
        print(msg)
        messages.info(request,'MARKS UPDATED')
        return redirect('/../evaluator/scanqr')
    
    msg = 'Upload marks'
    print(msg)
    messages.info(request,'Upload marks')
    return render(request, "EVALUATOR PAGE\input.html")

def back(request):
    return render(request, "EVALUATOR PAGE\scan.html")
