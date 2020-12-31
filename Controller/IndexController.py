from flask import Blueprint, render_template
from flask_login import current_user, login_required
from Service.FoodService import FoodService
from Service.OrderService import OrderService

main = Blueprint("index", __name__)
foodservice = FoodService()
orderservice = OrderService()


@main.route("/index")
def index():
    popfoods = foodservice.getTopSailing(3)
    print(popfoods)
    orders, foodlist = orderservice.getOrderById(current_user.id)
    return render_template("index.html", popfoods=popfoods, orders=orders, foodlist=foodlist)
