# IDK WHAT THE IMPORTS ARE
from abc import abstractclassmethod
from math import perm
from os import curdir
from sqlite3.dbapi2 import Cursor
from django.http.response import JsonResponse
from django.shortcuts import render
from django.http import HttpResponse
from django.core.mail import send_mail
import requests
import sqlite3
import datetime
import json
#-----------Connection to the Database----
# Need to add this cuz of an error. Reason unkonwn.
link = sqlite3.connect("db.sqlite3",check_same_thread=False)
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
        email       = request.session['email']
        start_date_str  = request.session['fromDate']
        end_date_str    = request.session['toDate']

        # String to Datetime
        x,y,z = [int(i) for i in start_date_str.split("-")]
        start_date  = datetime.date(x,y,z)
        x,y,z = [int(i) for i in end_date_str.split("-")]
        end_date    = datetime.date(x,y,z)

        rooms_booked = []
        room_types =  [[request.session['number_deluxe'],"Deluxe"],
                            [request.session['number_luxury'],"Luxury"],
                            [request.session['number_presidential'],"Presidential"]]
        cursor.execute("""
                        SELECT id 
                        FROM HotelManagement_user
                        WHERE email = :mail""", {'mail':email})
        user_id = cursor.fetchall()

        # IF a user exists:
        if user_id != None and user_id != []:
            user_id = user_id[0][0]         #Double Nested ID god damn

            for pair in room_types:
                # print(type(pair[0]))
                if pair[0] == '':
                    rooms = 0
                else:
                    rooms = int(pair[0])        #This was a string bruh
                room_type = pair[1]

                # WHY was i doing this?
                # To get least minimum rooms to satisfy
                # NOW take ALL and make life easier           
                cursor.execute(""" SELECT room_id,end_date FROM HotelManagement_room
                                WHERE room_type = :suite AND
                                is_empty = 1
                                LIMIT :limit;""",{'suite':room_type,'limit':100}) #'limit':rooms

                availableRooms = cursor.fetchall()

                final_list = []
                if availableRooms != []:
                    for myRoom,myDate in availableRooms:
                        if myDate == '':
                            myDate = datetime.date(2000,1,1)
                        final_list.append([myRoom,myDate])

                # If a room of given category is available
                if availableRooms != None and availableRooms != [] and len(availableRooms) >= rooms:
                    total_booked = 0
                    for room,date in final_list:
                        # print("GOT HERE!")
                        # print(total_booked, rooms)
                        if total_booked < rooms:
                            toggle = 0
                            cursor.execute("""
                                            SELECT end_date FROM HotelManagement_schedule
                                            WHERE room_booked = :id ORDER BY end_date DESC LIMIT 1;""",{'id':room})
                            roomExist = cursor.fetchall()

                            if roomExist == [] or roomExist[0][0] < end_date_str:   #See if comparision is correct
                                rooms_booked.append([room,room_type])
                                toggle = 1
                                # START BOOKING ROOMS
                            else:
                                cursor.execute("""
                                            SELECT start_date,end_date FROM HotelManagement_schedule
                                            WHERE room_booked = :id ORDER BY end_date DESC;""",{'id':room})
                                checkList = cursor.fetchall()
                                # print("YOOOOOOOOOOOOOOOOOOO",checkList)
                                if checkList != []:
                                    for indx in range(len(checkList)-1):
                                        if checkList[indx][1] < start_date_str and end_date_str < checkList[indx+1][0]:
                                            toggle = 1

                            if toggle == 1:
                                total_booked += 1
                            


        print("ROOMS BOOKED->",rooms_booked)
        return rooms_booked
    return None
# -------------------------------------------------------------
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
                            """,{'cust_id':None,'date':None,'bool':True,'id':None,'type':None,'today':str(today)})

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

def updateAllTables(email,fromDate,toDate,room_list):

    cursor.execute("""
                        SELECT id 
                        FROM HotelManagement_user
                        WHERE email = :mail""", {'mail':email})
    user_id = cursor.fetchall()

        # IF a user exists:
    if user_id != None and user_id != []:
        user_id = user_id[0][0]         #Double Nested ID
        room_list = json.loads(room_list)
        print("SzexY BREASST",type(room_list))

        if len(room_list) > 0:
            for values in room_list:
                room_id,room_type = values[0],values[1]
                with link:
                    cursor.execute("""
                                    INSERT INTO HotelManagement_schedule 
                                    (customer_id,start_date,end_date,room_booked,room_type)
                                    VALUES        (:id,:s_date,:e_date,:room_no,:r_type);"""
                                    ,{'id':user_id,'s_date':str(fromDate),'e_date':str(toDate),
                                    'room_no':room_id,'r_type':room_type})
        
        room_types = ["Deluxe","Luxury","Presidential"]
        allrooms = ''
        for room_id,room_type in room_list:
            for room in room_types:
                if room in room_type:
                    allrooms = allrooms + room + " "

            with link:
                cursor.execute("""
                                UPDATE HotelManagement_user
                                SET rooms = :allRooms
                                WHERE id = :user_id""",{'rooms':allrooms,'id':user_id})
