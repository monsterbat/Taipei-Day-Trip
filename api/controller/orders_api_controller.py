from flask import *
from MySQL_con import *

import sys
sys.path.append('api/module')
import booking_api_module
import orders_api_module

orders_api_controller = Blueprint(
    "orders_api_controller",
    __name__,
    static_folder="static",
    static_url_path="/static",
)
jwt_key = "key"
@orders_api_controller.route("/api/orders",methods=["POST"])
def orders():
    # jwt verify
    user_id = booking_api_module.verify_booking()   
    # Get token
    token = request.cookies.get('token')
    # check token with login or not
    if token == None:
        no_login_msg = jsonify({
            "error":True,
            "message":"使用者未登入"
        })
        return no_login_msg,403   
    try:  
        booking_msg = orders_api_module.get_orders_post(user_id)
        return booking_msg
    except:
        errorr_message = jsonify({
        "error": True,
        "message": "伺服器內部錯誤"
        })
        return errorr_message,500

@orders_api_controller.route("/api/orders/<orderNumber>",methods=["GET"])
def orderNumber(orderNumber):
    # Get token
    token = request.cookies.get('token')
    # check token with login or not
    if token == None:
        no_login_msg = jsonify({
            "error":True,
            "message":"使用者未登入"
        })
        return no_login_msg,403   
    try:
        orderNumber_msg = orders_api_module.get_orderNummber_get(orderNumber)
        return orderNumber_msg,200
    except:
        errorr_message = jsonify({
        "error": True,
        "message": "伺服器內部錯誤"
        })
        return errorr_message,500

@orders_api_controller.route("/api/orders/history/<user_id>",methods=["GET"])
def orderHistory(user_id):
    token = request.cookies.get('token')
    
    # check token with login or not
    if token == None:
        no_login_msg = jsonify({
            "error":True,
            "message":"使用者未登入"
        })
        return no_login_msg,403   
    try:
        orderHistory = orders_api_module.get_orderHistory_get(user_id)
        return orderHistory,200
    except:
        errorr_message = jsonify({
        "error": True,
        "message": "伺服器內部錯誤"
        })
        return errorr_message,500