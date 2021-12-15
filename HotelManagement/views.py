from os import curdir
from sqlite3.dbapi2 import Cursor
from django.http.response import JsonResponse
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.mail import send_mail
import requests
from string import ascii_lowercase, ascii_uppercase, digits
from random import choices
from .models import User, Room, Schedule    
import sqlite3
import HotelManagement


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
        validity = request.GET.get('valid')
        print(validity, type(validity), int(validity))
        validity = int(validity)
        if validity == 1:
            
            db = sqlite3.connect('db.sqlite3')
            cur = db.cursor()

            cur.execute('''
            SELECT email FROM HotelManagement_user;
            ''')

            email_list = cur.fetchall()
            email_list = [e[0] for e in email_list]
            print(email_list)

            if email in email_list:

                responseData = {
                    'message' : 'Email already in use'
                }
                
            else:

                responseData = {
                    'message' : 'Accepted'
                }
                user_data = User(name = username, email = email, encrypt_pwd = password)
                user_data.save()

        else:
            responseData = {
                'message' : 'Not accepted'
            }
    # return render(request, 'HotelManagement/reg_result.html')
    return JsonResponse(responseData)
    
def room(request):
    if request.method == "POST":
        # GET USERNAME IS ACTUALLY EMAIL
        email = request.POST.get('username', None)
        password = request.POST.get('password', None)

        context_content = {
            "email" : email
        }

        # CONNECTING TO THE DB AND MODIFYING RETURN CONDITION
        link = sqlite3.connect("db.sqlite3")
        def list_factory(cursor, row):
            lst = []
            for idx, col in enumerate(cursor.description):
                lst.append(row[idx])
            return lst
        link.row_factory = list_factory
        cursor = link.cursor()


        # CHECK IF USER IN DATABASE
        with link:
            cursor.execute("""
            SELECT email FROM HotelManagement_user WHERE email LIKE :electmail""",{'electmail':email})

            values = cursor.fetchone()
            print(f"LINE 147 views.py {values}")
            if values == [] or values == None:
                # WHAT TO DO IF USER NOT FOUND
                return render(request, 'HotelManagement/login.html')
            if values[0] != email:
                # WHAT TO DO IF INVALID EMAIL
                return render(request, 'HotelManagement/login.html')
            else:
                # CHECK PASSWORD
                cursor.execute("""
                SELECT encrypt_pwd FROM HotelManagement_user WHERE email LIKE :electmail""",{'electmail':email})

                psswrd = cursor.fetchone()
                if psswrd != [] and psswrd != None:
                    print(f"LINE 159 views.py {psswrd}")

                    psswrd = psswrd[0]
                    if psswrd == password:
                        # -------------
                        # CHECK IF USER HAS BOOKED A ROOM
                        with link:
                            cursor.execute("""
                            SELECT rooms FROM HotelManagement_user where email LIKE :electmail""",{'electmail':email})

                            roomBook = cursor.fetchone()
                            # IF NOT BOOKED
                            if roomBook != None and roomBook!= [] and roomBook[0] == "{}":
                                # REDIRECT TO BOOKING ROOM
                                return render(request, 'HotelManagement/room.html', context_content)
                            else:
                                # DO SOMETHING idk lmao
                                # ALREADY BOOKED ROOM
                                return render(request, 'HotelManagement/login.html')
                
                    else:
                        # WHAT TO DO IF PASSWORD INCORRECT
                        return render(request, 'HotelManagement/login.html')

                else:
                    # IF PASSWORD NOT FOUND
                    return render(request, 'HotelManagement/login.html')
            
            

       
    else:
        return render(request, 'HotelManagement/login.html')

def room_list(request):

    return render(request, 'HotelManagement/room_list.html')

