from os import name
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home-page"),
    path('login/', views.login, name="login-page"),
    path('verify/', views.verify, name="verification-page"),
    path('register/', views.register, name="registration-page"),
    path('reg_result/', views.reg_result, name="reg_result"),
    path('book_room/', views.room, name="book_room"),
    path('room_list/', views.room_list, name="room_list"),
    path('user_profile/', views.user_profile, name="user_profile")
]