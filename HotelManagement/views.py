from django.http.response import JsonResponse
from django.shortcuts import render
from django.http import HttpResponse
from django.core.mail import send_mail
import requests
from string import ascii_lowercase, ascii_uppercase, digits
from random import choices
from .models import User, Room, Schedule

import HotelManagement
# Create your views here.
# global arr
# arr = {
#     "Name" : None,
#     "Email" : None,
#     "phone_num" : None,
#     "PWD": None,
#     "rooms": None,
#     "checkin": None,
#     "checkout":None,
#     "verification_code": None
# }

def home(request):
    return render(request, 'HotelManagement/index.html')

def login(request):
    return render(request, 'HotelManagement/login.html')

def register(request):  
    return render(request, 'HotelManagement/register.html')

def verify(request):
    context = {
                "Name" : None,
                "Email" : None,
                "PWD": None,
                "verification_code": None
              }

    if request.method == "POST":
        Name = request.POST.get('Name', '')
        Email = request.POST.get('Email', '')
        # phone_num = request.POST.get('PhoneNo','')
        PWD = request.POST.get('PWD', '')
        print(Email)

        random_str = "".join(choices(ascii_uppercase + ascii_lowercase + digits, k=6))
        # random_str = request.POST.get('Verification Code', '')

        url = "https://email-sender1.p.rapidapi.com/"

        querystring = {"txt_msg":"test of the body","to":Email, "from":"Team 20","subject":"OTP verification","html_msg":f"<html><body><b>Welcome! {Name} to Ocean Pearl</b><br>{random_str}</body></html>"}

        headers = {
        'content-type': "application/json",
        'x-rapidapi-host': "email-sender1.p.rapidapi.com",
        'x-rapidapi-key': "f4a006106dmshc46a4e2a30f153dp1a2d06jsn7506f81db2ee"
        }

        payload = """{\r
                      \"key1\": \"value\",\r
                      \"key2\": \"value\"\r
                     }"""

        response = requests.request("POST", url, data=payload, headers=headers, params=querystring)
        print(response.text)

        context["Name"] = Name
        context["Email"] = Email
        context["PWD"] = PWD
        context["verification_code"] = random_str

    return render(request, 'HotelManagement/verify.html', context)

def reg_result(request):
    if request.method == "GET":
        username = request.GET.get('name', None)
        email = request.GET.get('email', None)
        password =request.GET.get('password', None)

        print(username, email, password)

        if request.GET.get('valid') == 1:
            
            user_data = User(name = username, email = email, encrypt_pwd = password)
            user_data.save()

            responseData = {
                'message' : 'Accepted'
            }
        else:
            responseData = {
                'message' : 'Not accepted'
            }
    # return render(request, 'HotelManagement/reg_result.html')
    return JsonResponse(responseData)
    
