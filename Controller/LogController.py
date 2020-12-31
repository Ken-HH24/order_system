from flask import Blueprint, render_template, request
from flask_login import current_user, logout_user
from Service.OrderService import OrderService
from Service.FoodService import FoodService
from Service.UserService import UserService

logmanager = Blueprint("loginout", __name__)
orderservice = OrderService()
foodservice = FoodService()
userservice = UserService()


@logmanager.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        res = UserService.authentication(username, password)
        if res is False:
            return render_template("login.html", login_error=True)
        else:
            popfoods = foodservice.getTopSailing(3)
            orders, foodlist = orderservice.getOrderById(current_user.id)
            return render_template('index.html', popfoods=popfoods, orders=orders, foodlist=foodlist)
    return render_template("login.html")


@logmanager.route('/logout', methods=['GET'])
def logout():
    logout_user()
    return render_template("login.html")


@logmanager.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        password = request.form['password']
        password2 = request.form['password2']
        if password != password2:
            return render_template("registration.html", password_error=True)
        name = request.form['name']
        username = request.form['username']
        phone = request.form['phone']
        if password == "" or username == "" or name == "" or phone == "":
            return render_template("registration.html", complete_error=True)
        elif userservice.findRepeatedName(username) is False:
            return render_template("registration.html", repeated_name=True)
        else:
            userservice.insertUser(name, phone, username, password)
            return render_template("login.html")
    return render_template("registration.html")
