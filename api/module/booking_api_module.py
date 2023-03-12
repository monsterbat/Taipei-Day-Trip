import sys
sys.path.append('api/function')

from MySQL_con import *
from flask import *
import jwt

from dotenv import load_dotenv
import os
load_dotenv()
jwt_key = os.getenv("jwt_key")

def verify_booking():
    # Get token
    token = request.cookies.get('token')
    # check token with login or not
    if token == None:
        no_login_msg = jsonify({
            "error":True,
            "message":"使用者未登入"
        })
        return no_login_msg,403

    # decode token know the user inf
    token_data = jwt.decode(token, jwt_key, algorithms="HS256")
    user_email = token_data["email"]
    sql_command="""
    SELECT id,name,email
    FROM user 
    WHERE email=%s;
    """
    value_input = (user_email,)
    user_info = query_data(sql_command,value_input)
    user_id = user_info[0]["id"]

    if user_info == []:
        verify_msg = jsonify({
            "error": True,
            "message": "token 有誤"
        })
        return verify_msg,401
    return user_id

def get_booking_get(user_id):
    data = {"data":None}
    # Booking inf
    sql_command="""
    SELECT id,user_id,attraction_id,date,time,price
    FROM booking 
    WHERE user_id=%s;
    """
    value_input = (user_id,)
    booking_info = query_data(sql_command,value_input)
    if booking_info != []:
        # Attraction inf
        attraction_id = booking_info[0]["attraction_id"]

        sql_command="""
        SELECT id,name,address
        FROM attraction 
        WHERE id=%s;
        """
        value_input = (attraction_id,)
        attraction_info = query_data(sql_command,value_input)
        # Attraction img inf
        sql_command="""
        SELECT attraction_id,images FROM attraction
        INNER JOIN attraction_image ON attraction.id=attraction_image.attraction_id
        WHERE attraction_id = %s;
        """
        value_input=(attraction_id,)
        attraction_img = query_data(sql_command,value_input)
        data = {
            "data":{
                "attraction":{
                    "id": attraction_info[0]["id"],
                    "name":attraction_info[0]["name"],
                    "address":attraction_info[0]["address"],
                    "image":attraction_img[0]["images"]
                },
                "date":booking_info[0]["date"],
                "time":booking_info[0]["time"],
                "price":int(booking_info[0]["price"])
            }
        }

    return data,200

def delete_booking_inf(user_id):
    # Delete previous data
    sql_command = """
    DELETE FROM booking 
    WHERE user_id = %s;
    """
    value_input = (user_id,)
    insert_or_update_data(sql_command,value_input)   

def get_booking_post(user_id):
    # Insert data
    booking_data = request.get_json()
    attraction_id = booking_data["attractionId"]
    date = booking_data["date"]
    time = booking_data["time"]
    price = booking_data["price"]

    sql_command = """
    INSERT INTO booking (user_id, attraction_id, date, time, price)
    VALUES (%s,%s,%s,%s,%s);
    """
    value_input = (user_id,attraction_id,date,time,price)
    insert_or_update_data(sql_command,value_input)
    data=jsonify({"ok":True})
    return data,200