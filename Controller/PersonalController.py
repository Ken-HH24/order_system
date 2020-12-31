from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user
from Service.OrderService import OrderService
from Service.UserService import UserService

individual = Blueprint("personal", __name__)
ordersevice = OrderService()
userservice = UserService()


@individual.route("/personal", methods=['GET'])
def show():
    orders, foodlist = ordersevice.getOrderById(current_user.id)
    return render_template("personal.html", orders=orders, foodlist=foodlist)


@individual.route("/alterusername", methods=['POST'])
def updateUsername():
    newname = request.form.get('username')
    if newname == "":
        flash("请输入新的用户名")
    elif userservice.findRepeatedName(newname):
        flash("用户名重复")
    else:
        userservice.updateUsername(current_user.id, newname)
    return redirect(url_for('personal.show'))


@individual.route("/alterpassword", methods=['POST'])
def updatePassword():
    newpassword = request.form.get('password')
    if newpassword == "":
        flash("请输入新的密码")
    else:
        userservice.updatePassword(current_user.id, newpassword)
    return redirect(url_for('personal.show'))
