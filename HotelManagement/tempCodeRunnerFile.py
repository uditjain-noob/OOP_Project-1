#-----------Connection to the Database----
import sqlite3
import datetime
link = sqlite3.connect("db.sqlite3")
def list_factory(cursor, row):
    lst = []
    for idx, col in enumerate(cursor.description):
        lst.append(row[idx])
    return lst
link.row_factory = list_factory
cursor = link.cursor()

with link:
    roomTypes = ["Deluxe", "Luxury", "Presidential"]
    for i in range(101, 201):
        if (i + 4) % 35 == 0:
            tempType = roomTypes.pop(0)

        cursor.execute("""
            UPDATE HotelManagement_room
            SET room_type = :room
            WHERE room_id = :id
        """,{'room':tempType,'id':i})
rooms = 3
room_type = "Presidential"
start_date = datetime.date.today()
end_date = datetime.date.today()
user_id = 102

cursor.execute(""" SELECT room_id, end_date FROM HotelManagement_room
                    WHERE room_type = :suite AND
                    is_empty = :condition
                    LIMIT :limit;""",{'suite':room_type,'condition':True,'limit':rooms})

availableRooms = cursor.fetchall()
print(availableRooms)

if availableRooms != None and availableRooms != [] and len(availableRooms) == rooms:
    # Say Rooms are Available (or ur wish idfc brah)
    print("Rooms Available!")
    for room,date in availableRooms:
        # START BOOKING ROOMS
        with link:
            cursor.execute("""
                            SELECT end_date FROM HotelManagement_schedule
                            WHERE room_booked = :id ORDER BY end_date DESC LIMIT 1;""",{'id':room})
            roomExist = cursor.fetchall()
            print(roomExist)
            if roomExist == [] or roomExist[0] < end_date:
                cursor.execute("""
                                INSERT INTO HotelManagement_schedule 
                                (customer_id,start_date,end_date,room_booked,room_type)
                                VALUES  (:id,:s_date,:e_date,:room_no,:r_type);"""
                                ,{'id':user_id,'s_date':str(start_date),'e_date':str(end_date),
                                'room_no':room,'r_type':room_type})


