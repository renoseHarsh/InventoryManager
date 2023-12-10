from django.contrib import admin
from django.urls import path, include 
from .views import *

urlpatterns = [
    path('register/', registerPage, name='register'),
    path('login/', loginPage, name='login'),
    path('logout/', logoutUser, name='logout'),
    path('', home, name='home'),
    path('userInfo/<str:userId>/', userInfoOwn, name='userInfo'),
    path('userInfo/', userInfoEmp, name='userInfo'),
    path('statement/<str:STcode>/', showST, name='showST'),
    path('location/<int:location_id>/', locationInfo, name='locationInfo'),
    path('update_location/', update_location, name='update_location'),
    path('update_assigned/', update_assigned, name='update_assigned'),
    path('update_FullName/', update_FullName, name='update_FullName'),

]