import sys
sys.path.append('api/function')
import booking_api_module
from MySQL_con import *
from flask import *
# .env 
from dotenv import load_dotenv
import os
load_dotenv()
tappay_partner_key = os.getenv("tappay_partner_key")

import datetime
import requests

def get_orders_post(user_id):
    current_time_code = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    # Insert data
    orders_data = request.get_json()
    prime = orders_data["prime"]
    price = orders_data["order"]["price"]
    attraction_id = orders_data["order"]["trip"]["attraction"]["id"]
    attraction_name = orders_data["order"]["trip"]["attraction"]["name"]
    attraction_address = orders_data["order"]["trip"]["attraction"]["address"]
    attraction_image = orders_data["order"]["trip"]["attraction"]["image"]
    order_date = orders_data["order"]["trip"]["date"]
    order_time = orders_data["order"]["trip"]["time"]
    contact_name = orders_data["order"]["contact"]["name"]
    contact_email = orders_data["order"]["contact"]["email"]
    contact_phone = orders_data["order"]["contact"]["phone"]

    unite_id_len = str(user_id).rjust(7,"0")
    order_number = str(current_time_code+unite_id_len)
    partner_key = tappay_partner_key

    url = "https://sandbox.tappaysdk.com/tpc/payment/pay-by-prime"
    header= {
      "Content-Type": "application/json",
      "x-api-key": partner_key
    }   
    data = {
        "prime": prime,
        "partner_key": partner_key,
        "merchant_id": "SC_CTBC",
        "details":"TapPay Test",
        "order_number":order_number,
        "amount": price,
        "cardholder": {
            "phone_number": contact_phone,
            "name": contact_name,
            "email": contact_email
        },
        "remember": False
    }

    tappay_request = requests.post(url, json.dumps(data), headers = header)
    tappay_request = tappay_request.json()
    if tappay_request["status"] == 0:
        pay_ststus = "已付款"
        pay_msg = "付款成功"    
        sql_command = """
        INSERT INTO orders (user_id, order_number, pay_status,contact_phone,contact_name,contact_email,attraction_id,attraction_name,attraction_address,attraction_image,order_date,order_time)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);
        """
        value_input = (user_id,order_number,pay_ststus,contact_phone,contact_name,contact_email,attraction_id,attraction_name,attraction_address,attraction_image,order_date,order_time)
        insert_or_update_data(sql_command,value_input)

        respon_msg = jsonify({
            "data": {
                "number": order_number,
                "payment": {
                    "status": tappay_request["status"],
                    "message": pay_msg
                }
            }
        })
        return respon_msg,200
    else:
        pay_ststus = "未付款"
        pay_msg = "付款失敗"
        sql_command = """
        INSERT INTO orders (user_id, order_number, pay_status,contact_phone,contact_name,contact_email)
        VALUES (%s,%s,%s,%s,%s,%s);
        """
        value_input = (user_id,order_number,pay_ststus,contact_phone,contact_name,contact_email)
        insert_or_update_data(sql_command,value_input)

        respon_msg = jsonify({
            {
            "error": True,
            "message": "訂單建立失敗，輸入不正確或其他原因"
            }
        })
        return respon_msg,400

def get_orderNummber_get(orderNumber):
    sql_command="""
    SELECT user_id, order_number, pay_status,contact_phone,contact_name,contact_email
    FROM orders 
    WHERE order_number=%s;
    """
    value_input = (orderNumber,)
    orders_info = query_data(sql_command,value_input)
    
    user_id = orders_info[0]["user_id"]
    order_number = orders_info[0]["order_number"]
    status = orders_info[0]["pay_status"]
    if status == "已付款":
        order_status = 1
    
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
        "data": {
            "number": order_number,
            "price": booking_info[0]["price"],
            "trip": {
            "attraction": {
                "id": booking_info[0]["attraction_id"],
                "name": attraction_info[0]["name"],
                "address": attraction_info[0]["address"],
                "image": attraction_img[0]["images"]
            },
            "date": booking_info[0]["date"],
            "time": booking_info[0]["time"]
            },
            "contact": {
            "name": orders_info[0]["contact_name"],
            "email": orders_info[0]["contact_email"],
            "phone": orders_info[0]["contact_phone"]
            },
            "status": order_status
        }
    }
    booking_api_module.delete_booking_inf(user_id)

    return data

def get_orderHistory_get(user_id):
    sql_command="""
    SELECT user_id, order_number, pay_status,contact_phone,contact_name,contact_email,attraction_id,attraction_name,attraction_address,attraction_image,order_date,order_time
    FROM orders 
    WHERE user_id=%s;
    """
    value_input = (user_id,)
    orders_info = query_data(sql_command,value_input)
    return orders_info

