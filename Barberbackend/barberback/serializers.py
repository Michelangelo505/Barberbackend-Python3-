# -*- coding: utf-8 -*-


from rest_framework import serializers
from .models import *


class UserInfo(object):

    def __init__(self, token, phone, nUser):
        self.token = token
        self.phone = phone
        self.nUser = nUser

class SerializerUserInfo(serializers.Serializer):
                        
    token = serializers.CharField()        
    phone = serializers.CharField()
    nUser = serializers.CharField()

class SerializerListNews(serializers.ModelSerializer):
    class Meta:
        model = BarberNews
        fields = ['bTitleNews', 'bTextNews', 'bNewsDate']
        
class SerializerListServices(serializers.ModelSerializer):
    class Meta:
        model = BarberService
        fields = ['id', 'bService', 'bPrice', 'bService_text']        

class SerializerListMasters(serializers.ModelSerializer):
    class Meta:
        model = BarberMasters
        fields = ['id', 'bMaster', 'bMaster_text', 'bDateBegin', 'bDateEnd']

class SerializerListServiceTime(serializers.ModelSerializer):
    class Meta:
        model = ServiceTime
        fields = ['id', 'bTime', 'bTimeStatus']        

class SerializerStopTime(serializers.ModelSerializer):
    class Meta:
        model = MasterTimeTable
        fields = ['bTimeMaster', 'bDateEnd']      


class SerializerOrder(serializers.ModelSerializer):
    class Meta:
        model = UserOrders             
        fields = '__all__'
        depth = 1

def funcname(self, parameter_list):
    raise NotImplementedError        