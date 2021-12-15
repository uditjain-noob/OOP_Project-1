# IDK WHAT THE IMPORTS ARE
from os import curdir
from sqlite3.dbapi2 import Cursor
from django.http.response import JsonResponse
from django.shortcuts import render
from django.http import HttpResponse
from django.core.mail import send_mail
import requests
from string import ascii_lowercase, ascii_uppercase, digits
from random import choices

from HotelManagement.views import room
from .models import User, Room, Schedule    
import sqlite3
import HotelManagement
import datetime
#-----------Connection to the Database----
link = sqlite3.connect("db.sqlite3")
def list_factory(cursor, row):
    lst = []
    for idx, col in enumerate(cursor.description):
        lst.append(row[idx])
    return lst
link.row_factory = list_factory
cursor = link.cursor()
# ------------------------------------------
def bookRoom(request):
    # assuming its a post/get request
    # else get me the customer name/email/id somehow
    if request.method == "GET":
        # GET USERNAME IS ACTUALLY EMAIL
        email = request.GET.get('username', None)
        rooms = 3
        room_type = "Deluxe"
        start_date = datetime.date.today()
        end_date = datetime.date.today()
        cursor.execute("""
                        SELECT id 
                        FROM HotelManagement_room 
                        WHERE email = :mail""", {'mail':email})
        user_id = cursor.fetchall()
        if user_id != None and user_id != []:
            user_id = user_id[0]
            cursor.execute(""" SELECT room_id,end_date FROM HotelManagement_room
                               WHERE room_type = :suite AND
                               is_empty = :condition
                               LIMIT :limit;""",{'suite':room_type,'condition':True,'limit':rooms})

            availableRooms = cursor.fetchall()
            if availableRooms != None and availableRooms != [] and len(availableRooms) == rooms:
                for room,date in availableRooms:
                    cursor.execute("""
                                    SELECT end_date FROM HotelManagement_schedule
                                    WHERE room_booked = :id ORDER BY end_date DESC LIMIT 1;""",{'id':room})
                    roomExist = cursor.fetchall()
                    if roomExist == [] or roomExist[0] < end_date:
                    # START BOOKING ROOMS
                        with link:
                            cursor.execute("""
                                            INSERT INTO HotelManagement_schedule 
                                            (customer_id,start_date,end_date,room_booked,room_type)
                                            VALUES        (:id,:s_date,:e_date,:room_no,:r_type);"""
                                            ,{'id':user_id,'s_date':str(start_date),'e_date':str(end_date),
                                            'room_no':room,'r_type':room_type})

# ------------------------------------------------------------
def LiveUpdate():
    today = datetime.date.today()
    #FLUSHING OUT OLD USERS
    with link:
        cursor.execute("""  UPDATE HotelManagement_room
                            SET customer_id = :cust_id,
                            end_date    = :date,
                            start_date  = :date,
                            is_empty    = :bool,
                            room_id     = :id,
                            room_type   = :type
                            WHERE end_date = :today
                            """,{'date':None,'bool':True,'id':None,'type':None,'today':str(today)})

    with link:
        cursor.execute(f"""
                        SELECT * 
                        FROM HotelManagement_schedule
                        WHERE start_date = {str(today)};
                        """)

        newEntries = cursor.fetchall()

        for entry in newEntries:
            cursor.execute(f""" 
                        UPDATE HotelManagement_room
                        SET customer_id = {entry[1]}
                        end_date    = {entry[2]},
                        start_date  = {entry[4]},
                        is_empty    = {False},
                        room_id     = {entry[3]},
                        room_type   = {entry[5]};
            """)
#--------------------------------------------------------------------
