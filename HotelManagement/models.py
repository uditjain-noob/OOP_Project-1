from django.db import models
from django.db.models.fields import CharField, IntegerField, DateField
from django.utils import timezone
# Create your models here.

class Room(models.Model):
    room_num = models.IntegerField(default=0, primary_key=True)
    room_type = models.CharField(max_length=50, default=" ")

class Schedule(models.Model):
    # id = models.IntegerField(default=0, primary_key=True)
    room_num = models.IntegerField(default=0)
    check_in = models.DateField(default = timezone.now)
    check_out = models.DateField(default = timezone.now)

class User(models.Model):
    # id = models.IntegerField(default=0, primary_key=True, auto_created=True)
    name = models.CharField(max_length=50, default=" ")
    email = models.CharField(max_length=100, default=" ")
    phone_num = models.CharField(max_length=10)
    encrypt_pwd = models.CharField(max_length=50, default=" ")
    rooms = models.CharField(max_length=150, default = " ")
