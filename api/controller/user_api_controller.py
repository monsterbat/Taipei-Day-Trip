from flask import *
import sys
sys.path.append('api/module')
import user_api_module

user_api_controller = Blueprint(
    "user_api_controller",
    __name__,
    static_folder="static",
    static_url_path="/static",
)

jwt_key = "key"
@user_api_controller.route("/api/user/auth", methods=["PUT","GET","DELETE","PATCH"])
def auth():
    if request.method == "GET":
        try:
            verify_msg = user_api_module.get_auth_get()
            return verify_msg,200

        except:
            errorr_message = {
                "error": True,
                "message": "伺服器內部錯誤"
            }
            return errorr_message,500
    if request.method == "PUT":
        try:
            verify_msg = user_api_module.get_auth_put()
            return verify_msg
            
        except:
            errorr_message = jsonify({
                "error": True,
                "message": "伺服器內部錯誤"
            })
            return errorr_message,500
    if request.method == "DELETE":
        try:
            token_del = Response('delete cookies')
            token_del = jsonify({"ok":True})
            token_del.set_cookie(key='token', value='', expires=0)
            return token_del
        except:
            errorr_message = {
                "error": True,
                "message": "伺服器內部錯誤"
            }
            return errorr_message,500
    if request.method == "PATCH":
        try:
            verify_msg = user_api_module.get_auth_patch()
            return verify_msg,200

        except:
            errorr_message = {
                "error": True,
                "message": "伺服器內部錯誤"
            }
            return errorr_message,500
@user_api_controller.route("/api/user", methods=["POST"])
def user():
    try:        
        verify_msg = user_api_module.get_user_post()
        return verify_msg
        
    except:
        errorr_message = jsonify({
            "error": True,
            "message": "伺服器內部錯誤"
        })
        return errorr_message,500
