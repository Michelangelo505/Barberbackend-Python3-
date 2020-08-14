from django.urls import path
from .adminpanelview import *
from .views import *


app_name = 'adminpanel'

urlpatterns = [
    path('', index.as_view(), name='index'),
    path('login', login.as_view(), name='login'),
    path('logout', logout.as_view(), name='logout'),
    path('profile/<str:username>/', profile.as_view(), name='profile'),
    path('registration', registUser.as_view(), name='registration'),
    path('successfully/<int:number>/', successfully.as_view(),name='successfully'),
    path('list_news', listNews.as_view(), name='list_news'),
    path('detail_new/<int:pk>', detailNew.as_view(), name='detail_new'),
    path('create_new', createNew.as_view(), name= 'create_new'),
    path('delete_new/<int:pk>', deleteNew.as_view(), name= 'delete_new'),
    path('update_new/<int:pk>', updateNew.as_view(), name= 'update_new'),
]