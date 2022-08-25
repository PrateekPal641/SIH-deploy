from asyncio.windows_events import NULL
from curses.ascii import NUL
from distutils.command.upload import upload
import email
from email.policy import default
from tkinter import CENTER
from unittest.util import _MAX_LENGTH
from django.db import models
from django.forms import ImageField
from django.contrib.auth.models import User 

from django.db import models
from django.utils import timezone
import os
from uuid import uuid4

def path_and_rename(instance, filename):
        upload_to = 'static/'
        ext = filename.split('.')[-1]
        # get filename
        if instance.username:
            filename = '{}.{}'.format(instance.username, ext)
        else:
            # set filename as random string
            filename = '{}.{}'.format(uuid4().hex, ext)
        # return the whole path to the file
        return os.path.join(upload_to,'c'+str(instance.center), filename)
# Create your models here.

class studata(models.Model):
    # user=models.OneToOneField(User, on_delete=models.CASCADE)
    appno=models.TextField('appno',max_length=30,default='')
    username = models.TextField('username',max_length=10, default = '')
    fullname=models.TextField('full_name',max_length=30,default='')
    dob=models.DateField('dob',default='2001-1-1')
    email=models.EmailField('email',max_length=30,default='')
    contact=models.TextField('contact',default='')
    gender=models.TextField('gender', default = '')
    city=models.TextField('city', default = '')
    state=models.TextField('state', default='')
    nationality = models.TextField('ntly', default = '')
    answerid = models.TextField('answerid',default = '')
    marks = models.TextField('marks', max_length = 3, default = '')
    remarks = models.TextField('remarks', default = '')
    center=models.TextField('center',default='')
    image=models.ImageField(upload_to=path_and_rename,null=True,blank=True)
    astatus=models.BooleanField('astatus',default=False)


    # @property
    # def image_url(self):
    #     if self.image:
    #         return getattr(self.photo, 'url', None)
    #     return None

    
    
    def __str__(self):
        return self.appno

    