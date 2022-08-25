from tkinter import Canvas
from django.db import models
from django.forms import CharField
import qrcode
from io import BytesIO
from django.core.files import File
from PIL import Image, ImageDraw

# Create your models here.

class qrc(models.Model):
    serialn=models.CharField(max_length=100)
    qr_code=models.FileField(upload_to='qrcode')

    def __str__(self):
        return str(self.serialn)


    # def save(self, *args, **kwargs):
    #     qrcode_img=qrcode.make(self.serialn)
    #     canvas=Image.new('RGB',(290,290),'white')
    #     draw = ImageDraw.Draw(canvas)
    #     canvas.paste(qrcode_img)
    #     fname=f'qr_code-{self.serialn}.png'
    #     buffer=BytesIO()
    #     canvas.save(buffer,'PNG')
    #     self.qr_code.save(fname,File(buffer),save=False)
    #     canvas.close()
    #     super().save(*args, **kwargs)




    
