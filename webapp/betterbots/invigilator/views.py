from email.mime import image
from re import X
from django.http import HttpResponse
from django.shortcuts import redirect, render
from pytz import country_timezones
from django.utils.datastructures import MultiValueDictKeyError
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from django.contrib import messages
import qrcode 
import PIL.Image
import cv2
from deepface import DeepFace
import os
from student.models import studata

from django.conf import settings
value = settings.BASE_DIR
# Create your views here.

post={}
path=""


def inhome(request):
    msg = "fghj"
    if request.method=="POST":
        username: str =  request.POST['Center_ID']
        password =  request.POST['password']
        centercode =  request.POST['centercode']
        password=str(password) 
        # print(username)
        # print(password)
        
        user =None
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_invigilator==False or user.center!=centercode:
                msg = 'Unauthorized'
                print(msg)
                messages.info(request,'User is UNAUTHORIZED!')
                print("UNAUTHORIZED")
                return redirect('/../invigilator/')
            global post 
            post['cid']=user.center
            global path
            path = os.getcwd() + str("\media\static")
            print(post)
            # global post
            # print(post) 
            path = os.path.join(path, post['cid'])
            login(request, user)
            return redirect('/../invigilator/scan')
        else:
            msg = 'invlaid credentials'
            print(msg)
            messages.info(request,'User is not registered!')
            return redirect('/../invigilator/')  
    return render(request, "INVIGILATOR\index.html")

def scan(request):
    if request.user.is_authenticated:
        return render(request, "INVIGILATOR\scan.html")
    else:
        msg = 'Unauthorized'
        print(msg)
        messages.info(request,'UNAUTHORIZED!')
        return redirect('/../invigilator/') 
    

def logo(request):
    logout(request)
    messages.info(request,'Successfully logged out!')
    return redirect('/../invigilator/')



def video_reader(request):
    cam = cv2.VideoCapture(0,cv2.CAP_DSHOW)
    detector = cv2.QRCodeDetector()
    data=""
    while True:
        _, img = cam.read()
        cv2.imshow("img", img)
        data, bbox, _ = detector.detectAndDecode(img)
        if data:
            print("QR Code detected-->", data)
            global post 
            post['aid']=data
            break
        if cv2.waitKey(1) == ord("q"):
            break
    cam.release()
    cv2.destroyAllWindows()

    if data=='':
        messages.error(request,'No code detected!! Please try again!')
        return redirect('/../invigilator/scan')

    cam = cv2.VideoCapture(0,cv2.CAP_DSHOW)

    while True:
        _, img = cam.read()
        cv2.imshow("img", img)
        if cv2.waitKey(1) == ord("s"):
            cv2.imwrite('image.jpg', img)
            break
    cam.release()
    cv2.destroyAllWindows()
    s = 0
    global path
    # print(os.path.join(path,file))
    for file in os.listdir(path):
        try:
            recognition = DeepFace.verify(img1_path="image.jpg", img2_path=os.path.join(path, file))
            if recognition['verified'] == True:
                file = file.replace('.png', '')
                file = file.replace('.jpg', '')
                file = file.replace('.jpeg', '')
                post['imgid']=file
                print('Verified!!! for the image', file)
                s = 1
                return redirect('/../invigilator/details')
        except:
            messages.error(request, 'No Face Detected')
            return redirect('/../invigilator/scan')

        recognition = DeepFace.verify(img1_path="image.jpg", img2_path=os.path.join(path, file))
        print(os.path.join(path, file))
        if recognition['verified'] == True:
            file = file.replace('.png', '')
            file = file.replace('.jpg', '')
            file = file.replace('.jpeg', '')
            post['imgid']=file
            print('Verified!!! for the image', file)
            s = 1
            return redirect('/../invigilator/details')
    if s == 0:
        print("No Data found -_-")
        messages.error(request,'No match found!! Please try again!')
        return redirect('/../invigilator/scan')
        
    # if data!="":
    #     return HttpResponse(data)

    
    
def details(request):
    global post 
    posts=studata.objects.get(username=post['imgid'])
    posts.astatus=True
    posts.answerid=post['aid']
    posts.save()
    print(posts.username)
    return render(request, "INVIGILATOR/finald.html",{'posts':posts})  

