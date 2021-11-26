from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home-page"),
<<<<<<< HEAD
    path('login/', views.login, name="login-page"),
    path('verify/', views.verify, name="verification-page"),
    path('register/', views.register, name="registration-page")
=======
    path('register/', views.register, name="registration-page"),
    path('verify/', views.verify, name="verification-page")
>>>>>>> 1dddead0bf26edd5cce765210c73f57648faddf8
]