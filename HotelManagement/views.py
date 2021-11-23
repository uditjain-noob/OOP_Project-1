from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.


def home(request):
    return render(request, 'HotelManagement/index.html')

def register(request):
    if request.method == "POST":
        Name = request.POST.get('Name', '')
        Email = request.POST.get('Email', '')
        phone_num = request.POST.get('PhoneNo','')
        PWD = request.POST.get('PWD', '')
        
        Reg = User(name = Name, )
    return render(request, 'HotelManagement/register.html')