from flask import Blueprint, render_template, request, redirect, url_for, flash
from Service.FoodService import FoodService
from Service.OrderService import OrderService

orders = Blueprint("order", __name__)
foodservice = FoodService()
orderservice = OrderService()


@orders.route("/order", methods=['GET'])
def show():
    foodlist = foodservice.getFoodByType()
    return render_template("order.html", foodlist=foodlist)


@orders.route("/order", methods=['POST'])
def giveorder():
    types = foodservice.getFoodType()
    foodids = [request.form.get(atype, None) for atype in types if request.form.get(atype, None) is not None]
    address = request.form.get("address", "")
    receiver = request.form.get("receiver", "")
    receiver_phone = request.form.get("receiver_phone", "")
    price = foodservice.calPrice(foodids)
    if address == "" or receiver == "" or receiver_phone == "":
        flash("请完善你的信息")
    elif len(foodids) == 0:
        flash("请选择你的食物")
    else:
        orderservice.insertOrder(price, address, receiver, receiver_phone, foodids)
    return redirect(url_for('order.show'))
