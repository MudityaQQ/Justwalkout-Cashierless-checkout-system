from django.contrib import admin
from django.urls import path
from .views import *
urlpatterns = [
    path('',home,name = "home"),
    path('register/',register,name = 'register'),
    path('login/',login,name = 'login'),
    path('logout/',logout,name = 'logout'),
    path('userNotFound/',userNotFound,name = 'userNotFound'),
    path('dashboard/<face_id>/',dashboard,name='dashboard'),
]
