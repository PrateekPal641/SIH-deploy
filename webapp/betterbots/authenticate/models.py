from asyncio.windows_events import NULL
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    application_no=models.TextField('application_no',default='')
    fullname=models.TextField('full_name',max_length=30,default='')
    # dob=models.DateField('dob',default='2001-1-1')
    email=models.EmailField('email',max_length=30,default='')
    contact=models.TextField('contact',  default='')
    gender = models.TextField('gender', default = '')
    cpassword=models.TextField('fpass', default='')
    center=models.TextField('center', default = '')
    # state=models.TextField('state', default='')
    # nationality = models.TextField('ntly', default = '')
    is_student=models.BooleanField('is_student',default=False)
    is_invigilator=models.BooleanField('is_invigilator',default=False)
    is_evaluator=models.BooleanField('is_evaluator',default=False)
    # image=models.ImageField(upload_to="static/STUDENTS PAGE/images/",null=True,blank=True)
    
    
    
