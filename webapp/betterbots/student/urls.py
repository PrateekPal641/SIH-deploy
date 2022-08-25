"""betterbots URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_view

from . import views

app_name="studenthome"
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.studenthome, name="studenthome"),
    path('application',views.application, name="application"),
    path('result',views.result,name="result"),
    path('profile',views.profile,name="profile"),
    path('logout1',views.logout1,name ="logout1")
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
