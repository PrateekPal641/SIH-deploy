from base64 import standard_b64decode
from dataclasses import dataclass
from re import X
import re
import os
import cv2
from deepface import DeepFace
from django.core.files.storage import default_storage

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
from django.contrib.auth.decorators import login_required
import uuid
User = get_user_model()

# Create your views here.


x=0

def studenthome(request):
    return render(request, "STUDENTS PAGE\home.html")

def application(request):
    global x
    if request.method=="POST":
        username =  request.POST['username']
        fname:str = request.POST['fname']
        dob: str =  request.POST['dob']
        mail:str = request.POST['mail']
        contact  =  request.POST['contact']
        gender:str = request.POST['gender']
        password:str =  str(request.POST['fpass'])
        cnfpass: str = str(request.POST['spass'])
        city:str = request.POST['city']
        state:str = request.POST['state']
        ntly:str = request.POST['ntly']

        if(password != cnfpass):
            messages.error(request, 'Password and Confirm password are not same!')
            return redirect('/student/application')
        if User.objects.filter(username=username).exists():
            messages.error(request, ' Sorry! Username is already taken')
            return redirect('/student/application')
        if len(request.FILES)==0:
            messages.error(request, 'Please insert an image')
            return redirect('/student/application')
        elif User.objects.filter(email=mail).exists():
            messages.error(request, ' Sorry! Email is already registered')
            return redirect('/student/application')
        

        appno="2022"+str(uuid.uuid4().node)[5:12]
        
        msg=None
        password=str(password)


        # if password !=cnfpass:
        #     try:
        #     except ValidationError:


            # return redirect('/../student/application/')

        myuser = User.objects.create_user(username = username,password=password)
        myuser.fullname=fname
       
        myuser.email=mail
        myuser.contact=contact
        myuser.gender=gender
       
        myuser.cpassword = password
        myuser.is_student=True
      

        myuser.application_no=appno
        # if len(request.FILES)!=0:
        #     myuser.image=request.FILES['image']
        
            
        
        myuser.save()

        sdata=studata()
        sdata.appno=appno
        sdata.username = username
        sdata.fullname=fname
        sdata.dob=dob
        sdata.email=mail
        sdata.contact=contact
        sdata.gender = gender
        sdata.city = city
        sdata.state = state
        sdata.answerid=id
        sdata.password = password
        sdata.center = x
        x+=1
        x%=2
        sdata.nationality = ntly
        
        s=0
        if len(request.FILES)!=0:
           
            
           #  Saving POST'ed file to storage
            file = request.FILES['image']
            file_name = default_storage.save(file.name, file)
            
            #  Reading file from storage
            file = default_storage.open(file_name)
            file_url = str(os.getcwd()+str(default_storage.url(file_name)))
            print(file_url)
            # print(file_url)
            # cv2.imwrite('image2.jpg', imgg)
            # cc='c'+str(x)
            # path1=os.getcwd() 
            # path1 = str(path1)+"/"+cc+ "/" + str(imgg)
            
            cam = cv2.VideoCapture(0,cv2.CAP_DSHOW)
            
            while True:
                _, img = cam.read()
                cv2.imshow("img", img)
                if cv2.waitKey(1) == ord("s"):
                    cv2.imwrite('image1.jpg', img)
                    break
            cam.release()
            cv2.destroyAllWindows()
            # # print(path1)
            # try:
            recognition = DeepFace.verify(img1_path="image1.jpg", img2_path=file_url)
            # print(imgg)
            if recognition['verified'] == True:
                sdata.image=file
                sdata.save()
                messages.success(request, 'Face verified!! SUCCESSFULLY REGISTERED')
                return redirect('/../student/result')
            else:
                messages.error(request, 'Face is not matching!! Please try again!')
                return redirect('/../student/application')
            # except:
            #     print("except")
            #     messages.error(request, 'No face detected!! Please try again!')
            #     return redirect('/../student/application')

        else:
            messages.error(request, 'Upload valid image file')
            return render(request, "STUDENTS PAGE\pply.html")
    
    return render(request, "STUDENTS PAGE\pply.html")


def result(request):
    msg = None
    
    if request.method=="POST":
        username =  request.POST['username']
        password =  request.POST['password']
        # password=str(password) 
        # username=str(username)
        user = authenticate(request,username=username, password=password)
        if user is not None:
            if user.is_student==False:
                msg = 'Unauthorized'
                print(msg)
                messages.info(request,'User is UNAUTHORIZED!')
                return redirect('/../student/result')
            posts=studata.objects.get(username=username)
            # posts.marks = 
            # print(posts.marks)
            if(posts.marks == ''):
                return render(request, "STUDENTS PAGE\iform.html",{'posts':posts, 'var': True}, )
            
             
            try:
                post=studata.objects.get(username=username)
                login(request, user)
                return render(request, "STUDENTS PAGE\iform.html",{'posts':post, 'var': False})
            except studata.DoesNotExist:
                msg = 'Unauthorized'
                print(msg)
                messages.info(request,'User is deleted!')
                return redirect('/../student/result')
                
            
            # posts={
            #     'username': post.username,    
            #     'fullname': post.fullname,
            #     'email': post.email,
            #     'contact': post.contact,
            #     'gender': post.gender,
            # }
            # print(posts)

            return render(request, "STUDENTS PAGE\iform.html",{'posts':post})
        else:
            messages.info(request,'User is not registered!')
            return redirect('/../student/result')
            
    return render(request, "STUDENTS PAGE\index.html")

def logout1(request):
    logout(request)
    messages.info(request,'Successfully logged out!')
    return redirect('/../student/result')

def profile(request):
    if request.user.is_authenticated:
        return render(request, "STUDENTS PAGE\iform.html")
    else:
        msg = 'Unauthorized'
        print(msg)
        messages.info(request,'UNAUTHORIZED!')
        return redirect('/../student/result')
        
# dict = {'Name':[],'Contact':[]}
# dict['name'].append()

# def create_df(request):
    

