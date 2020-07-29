from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(BarberProfile)
admin.site.register(BarberService)
admin.site.register(BarberNews)
admin.site.register(BarberUserSendNews)
admin.site.register(ServiceTime)
admin.site.register(BarberMasters)
admin.site.register(UserOrders)
admin.site.register(MasterTimeTable)