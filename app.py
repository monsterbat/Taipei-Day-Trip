"""
WeHelp BootCamp Assignemt - Stage 2 taipei_day_trip -*- main program -*-
Update date: 2022/12/14
Authored by SC Siao
"""

from flask import *
from flask_cors import CORS

import api.controller.attraction_api_controller as attraction_api_controller
import api.controller.user_api_controller as user_api_controller
import api.controller.booking_api_controller as booking_api_controller
import api.controller.orders_api_controller as orders_api_controller


app=Flask(
	__name__,
	static_folder="static",
    static_url_path="/static"
)
CORS(app)

app.register_blueprint(user_api_controller.user_api_controller)
app.register_blueprint(attraction_api_controller.attractions_api_controller)
app.register_blueprint(booking_api_controller.booking_api_controller)
app.register_blueprint(orders_api_controller.orders_api_controller)

# Pages
@app.route("/")
def index():
	return render_template("index.html")
@app.route("/attraction/<id>")
def attraction(id):
	return render_template("attraction.html")
@app.route("/booking")
def booking():
	token = request.cookies.get('token')
	if token == None:
		return redirect("/")
	return render_template("booking.html")
@app.route("/thankyou")
def thankyou():
	return render_template("thankyou.html")
@app.route("/memberCenter")
def memberCenter():
	return render_template("memberCenter.html")

app.debug = True
app.run(host = "0.0.0.0",port=3000)