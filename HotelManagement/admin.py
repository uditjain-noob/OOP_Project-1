from django.contrib import admin
from .models import Room, Schedule, User

# Register your models here.
admin.site.register(Room)
admin.site.register(Schedule)
admin.site.register(User)