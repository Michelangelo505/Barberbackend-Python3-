from django.shortcuts import render

# Create your views here.

from .models import BarberProfile, BarberUserSendNews, BarberNews, UserOrders, MasterTimeTable
from django.contrib.auth.models import User
from .serializers import *
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.authtoken.models import Token
import json
from datetime import datetime

from django.views.generic.edit import *

class GetUserInfo(APIView):
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated]

    def get(self, request, formant=None):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def post(self, request, format=None):
        lToken = Token.objects.get(user=request.user)

        lUserInfo = UserInfo(lToken, request.user.username, request.user.last_name)
        content = SerializerUserInfo(lUserInfo)
        return Response(content.data)


class GetListNewsUser(APIView):
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def post(self, request, format=None):
        # Определим есть ли новости для пользователя
        # lUser = request.user
        # lListPk = []
        # lNewsForSend = BarberUserSendNews.objects.filter(bNewsUser=lUser, bSend=False)
        # for newssend in lNewsForSend:
        #    lListPk.append(newssend.bNews.pk)

        # lNews = BarberNews.objects.filter(pk__in=lListPk).order_by('-bNewsDate')[:20]
        lNews = BarberNews.objects.all().order_by('-bNewsDate')[:2]
        content = SerializerListNews(lNews, many=True)
        return Response(content.data)

class CreateBarber(APIView):
    lNotExist = False

    def get(self, request, format=None):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def post(self, request, format=None):

        try:
            lUser = User.objects.get(username=request.data['phone'])
            lToken = Token.objects.get(user=lUser)
            b = UserInfo(token=lToken, phone=lUser.username, nUser=lUser.last_name)
            content = SerializerUserInfo(b)
            return Response(content.data)
        except User.DoesNotExist:
            self.lNotExist = True

        if self.lNotExist:
            # Создадим пользователя
            lUser = User.objects.create_user(request.data['phone'], 'lennon@thebeatles.com',
                                             request.data['phone'] + 'Qwsaq')
            lUser.last_name = ''
            lUser.save()

            lToken = Token.objects.create(user=lUser)
            # Здесь можно создать профиль если понадобиться
            # BarberProfile.objects.create(Barber_Phone=lUser.username, Barber_User=lUser)
            b = userinfo(token=lToken, phone=lUser.username, nUser=lUser.last_name)
            content = serializeruserinfo(b)
            return Response(content.data)


class GetListServices(APIView):
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def post(self, request, format=None):
        lServices = BarberService.objects.all()
        content = SerializerListServices(lServices, many=True)
        return Response(content.data)


class GetListMasters(APIView):
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def post(self, request, format=None):
        dt = request.data['date']
        ldate = datetime.strptime(dt, '%Y-%m-%d')
        lMasters = BarberMasters.objects.all()

        listmaster_pk = []
        for master in lMasters:
            listmaster_pk.append(master.pk)
        lstoplist = MasterTimeTable.objects.filter(bTimeMaster__in=listmaster_pk, bDateBegin__lte=ldate,
                                                   bDateEnd__gte=ldate)

        for master in lMasters:
            for lstop in lstoplist:
                if lstop.bTimeMaster == master:
                    master.bDateBegin = lstop.bDateBegin
                    master.bDateEnd = lstop.bDateEnd
        content = SerializerListMasters(lMasters, many=True)
        return Response(content.data)


class GetListServicesTime(APIView):
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def post(self, request, format=None):
        dt = request.data['date']
        ldate = datetime.date(datetime.strptime(dt, '%Y-%m-%d'))

        lServicesTime = ServiceTime.objects.all()
        lservicepk = []
        for lservtime in lServicesTime:
            lservicepk.append(lservtime.pk)

        userorders = UserOrders.objects.filter(bOrderTimeService__in=lservicepk,
                                               bOrderCreateDate=ldate,
                                               bOrderMaster=request.data['master_id'])
        lcount = userorders.count()
        ltimenow = datetime.time(datetime.now())
        lcurrent_date = datetime.date(datetime.today())
        for ltime in lServicesTime:
            if ltime.bTime < ltimenow and ldate == lcurrent_date:
                ltime.bTimeStatus = 'Запрещено'
            elif lcount == 0:
                ltime.bTimeStatus = 'Свободно'
            else:
                for lorder in userorders:
                    if ltime == lorder.bOrderTimeService:
                        ltime.bTimeStatus = 'Занято'
                        break
                    else:
                        ltime.bTimeStatus = 'Свободно'

        content = SerializerListServiceTime(lServicesTime, many=True)
        return Response(content.data)


class GetStopOutMaster(APIView):
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def post(self, request, format=None):
        ldate = datetime.strptime(request.data['date'], '%Y-%m-%d')
        lmaster = request.data['master_id']

        lstoplist = MasterTimeTable.objects.filter(bTimeMaster=lmaster, bDateBegin__lte=ldate, bDateEnd__gte=ldate)
        content = SerializerStopTime(lstoplist, many=True)
        return Response(content.data)


class CreateUserOrder(APIView):
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def post(self, request, format=None):

        dt = request.data['date']
        ldate = datetime.strptime(dt, '%Y-%m-%d')

        try:
            service = BarberService.objects.get(pk=request.data['service_id'])
        except BarberService.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        try:
            master = BarberMasters.objects.get(pk=request.data['master_id'])
        except BarberMasters.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        try:
            servicetime = ServiceTime.objects.get(pk=request.data['servicetime_id'])
        except ServiceTime.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        order = UserOrders(
            bOrderService=service,
            bOrderUser=request.user,
            bOrderMaster=master,
            bOrderCreateDate=ldate,
            bOrderTimeService=servicetime
        )

        inst = order.save()

        return Response(status=status.HTTP_201_CREATED)


class GetUsersOrder(APIView):
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def post(self, request, format=None):
        orders = UserOrders.objects.filter(bOrderUser=request.user).order_by('-bOrderCreateDate')[:10]
        content = SerializerOrder(orders, many=True)
        return Response(content.data)


class GetDataTotal(APIView):
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def post(self, request, format=None):

        '''
        self.get_list_masters()
        self.get_list_service()
        self.get_user_orders()
        self.get_list_news()
        '''

        dict_data = {}

        dict_data['news'] = self.list_news()
        dict_data['masters'] = self.list_masters(request)
        dict_data['services'] = self.list_services()
        dict_data['orders'] = self.list_orders(request)

        return Response(dict_data)

    def list_news(self):
        lNews = BarberNews.objects.all().order_by('-bNewsDate')[:20]
        content = SerializerListNews(lNews, many=True)
        return content.data

    def list_orders(self, request):
        orders = UserOrders.objects.filter(bOrderUser=request.user).order_by('bOrderCreateDate')[:10]
        content = SerializerOrder(orders, many=True)
        return content.data

    def list_services(self):
        lServices = BarberService.objects.all()
        content = SerializerListServices(lServices, many=True)
        return content.data

    def list_masters(self, request):
        dt = request.data['date']
        ldate = datetime.strptime(dt, '%Y-%m-%d')
        lMasters = BarberMasters.objects.all()

        listmaster_pk = []
        for master in lMasters:
            listmaster_pk.append(master.pk)
        lstoplist = MasterTimeTable.objects.filter(bTimeMaster__in=listmaster_pk, bDateBegin__lte=ldate,
                                                   bDateEnd__gte=ldate)

        for master in lMasters:
            for lstop in lstoplist:
                if lstop.bTimeMaster == master:
                    master.bDateBegin = lstop.bDateBegin
                    master.bDateEnd = lstop.bDateEnd
        content = SerializerListMasters(lMasters, many=True)
        return content.data