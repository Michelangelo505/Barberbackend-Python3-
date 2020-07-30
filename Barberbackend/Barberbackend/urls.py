"""Barberbackend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path

from barberback.views import *


urlpatterns = [
    path('admin', admin.site.urls),
    path('api/v1/gettotaldata', GetDataTotal.as_view()),
    path('api/v1/getuserinfo', GetUserInfo.as_view()),
    path('api/v1/register', CreateBarber.as_view()),
    path('api/v1/getlistnewsuser', GetListNewsUser.as_view()),
    path('api/v1/getlistservices', GetListServices.as_view()),
    path('api/v1/getlistmasters', GetListMasters.as_view()),
    path('api/v1/getlisttime', GetListServicesTime.as_view()),
    path('api/v1/getstoptime', GetStopOutMaster.as_view()),
    path('api/v1/createorder', CreateUserOrder.as_view()),
    path('api/v1/getorders', GetUsersOrder.as_view())
]
