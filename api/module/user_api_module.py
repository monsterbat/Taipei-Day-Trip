import sys
sys.path.append('api/function')
from MySQL_con import *
from flask import *
import jwt
import time
# Hash code to save password
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt()

from dotenv import load_dotenv
import os
load_dotenv()
jwt_key = os.getenv("jwt_key")
# jwt_key = "key"
def get_auth_get():
    token = request.cookies.get('token')
    # Judge with token or not
    if token == None:
        time_out_msg = jsonify({
            "data":None
        })
        return time_out_msg
    else:
        token_data = jwt.decode(token, jwt_key, algorithms="HS256")
        user_email = token_data["email"]
        
        sql_command="""
        SELECT id,name,email
        FROM user 
        WHERE email=%s;
        """
        value_input = (user_email,)
        user_info = query_data(sql_command,value_input)
        print(user_info)
        # Judge token right or wrong
        if user_info == []:
            verify_msg = jsonify({
                "error": True,
                "message": "token 有誤"
            })
        verify_msg = jsonify({
            "data":{
                "id":user_info[0]["id"],
                "name":user_info[0]["name"],
                "email":user_info[0]["email"]
            }
        })
        return verify_msg

def get_auth_put():
    sign_in_data = request.get_json()
    user_email = sign_in_data["email"]
    user_password = sign_in_data["password"]
    # Email check
    sql_command="""
    SELECT email, password
    FROM user 
    WHERE email=%s;
    """
    value_input = (user_email,)
    user_check = query_data(sql_command,value_input)
    check_password = ""
    if user_check != []:
        email_check = user_check[0]["email"]
        passowrd_check = user_check[0]["password"]
        # Password with hash coding
        check_password = bcrypt.check_password_hash(passowrd_check, user_password)
    if check_password == True:
        result=jsonify({"ok":True})
        # JWT token sgould not include password
        sign_in_data_email_only = {
            "email":sign_in_data["email"]
        }
        token = jwt.encode(sign_in_data_email_only, jwt_key, algorithm="HS256")
        
        cookie_sustain_days = 1
        result.set_cookie(key="token", value=token, expires=time.time()+cookie_sustain_days*60*60*24)
        return result,200
    else:
        error_msg = "帳號密碼"
        errorr_message = jsonify({
        "error": True,
        "message": error_msg+"有誤"
        })
        return errorr_message,400

def get_auth_delete():
    token_del = Response('delete cookies')
    token_del = jsonify({"ok":True})
    token_del.set_cookie(key='token', value='', expires=0)

def get_user_post():
    sign_up_data = request.get_json()
    user_name = sign_up_data["name"]
    user_email = sign_up_data["email"]
    user_password = sign_up_data["password"]
    
    # MySQL data Check
    # name check
    sql_command="""
    SELECT name
    FROM user 
    WHERE name=%s;
    """
    value_input = (user_name,)
    name_check = query_data(sql_command,value_input)

    # Email check
    sql_command="""
    SELECT email
    FROM user 
    WHERE email=%s;
    """
    value_input = (user_email,)
    email_check = query_data(sql_command,value_input)

    # Save password with hash coding		
    user_password = bcrypt.generate_password_hash(password=user_password)
    if name_check == [] and email_check == []:					
        sql_command = """
        INSERT INTO user (name, email, password)
        VALUES (%s,%s,%s);
        """
        value_input = (user_name,user_email,user_password)
        insert_or_update_data(sql_command,value_input)
        data=jsonify({"ok":True})
        return data,200

    else:
        error_msg = ""
        if name_check != []:
            error_msg = "名字"
        if email_check != []:
            error_msg = error_msg+" 信箱"
        errorr_message = jsonify({
        "error": True,
        "message": error_msg+"重複"
        })
        return errorr_message,400
def get_auth_patch():
    req_data=request.get_json()
    userId = req_data["userId"]
    newUserName = req_data["newUserName"]
    newUserMail = req_data["newUserMail"]
    oriUserPassword = req_data["oriUserPassword"]
    newUserPassword = req_data["newUserPassword"]
    
    if newUserName != None:
        sql_command="""
        UPDATE user 
        SET name= %s
        WHERE id= %s;
        """
        value_input=(newUserName,userId)
        insert_or_update_data(sql_command,value_input)
        req_msg = jsonify({
            "ok":True,
            "message":"使用者名稱變更完成"
            })
        return req_msg

    if newUserMail != None:
        sql_command="""
        UPDATE user 
        SET email= %s
        WHERE id= %s;
        """
        value_input=(newUserMail,userId)
        insert_or_update_data(sql_command,value_input)

        sign_in_data_email_only = {
            "email":newUserMail
        }
        req_msg = jsonify({
            "ok":True,
            "message":"使用者信箱變更完成"
            })
        token = jwt.encode(sign_in_data_email_only, jwt_key, algorithm="HS256")
        cookie_sustain_days = 1
        req_msg.set_cookie(key="token", value=token, expires=time.time()+cookie_sustain_days*60*60*24)
        return req_msg

    if oriUserPassword != None:
        sql_command="""
        SELECT password
        FROM user 
        WHERE id=%s;
        """       
        value_input = (userId,)
        user_check = query_data(sql_command,value_input)
        passowrd_check = user_check[0]["password"]
        passowrd_check = bcrypt.check_password_hash(passowrd_check, oriUserPassword)
        if passowrd_check == True:
            newUserPassword = bcrypt.generate_password_hash(password = newUserPassword)
            sql_command="""
            UPDATE user 
            SET password= %s
            WHERE id= %s;
            """
            value_input=(newUserPassword,userId)
            insert_or_update_data(sql_command,value_input)
            req_msg = jsonify({
                "ok":True,
                "message":"密碼更新完成"
                })
            return req_msg
        if passowrd_check == False:
            errorr_message = jsonify({
            "error": True,
            "message": "原始密碼輸入錯誤"
            })
            return errorr_message