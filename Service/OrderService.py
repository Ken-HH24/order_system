from DAO.OrderDao import Order, OrderRepository
from DAO.FoodRepository import Food, FoodRepository
from datetime import datetime
from flask_login import current_user

orderrep = OrderRepository()
foodrep = FoodRepository()


class OrderService:
    def getOrderById(self, userid):
        orders = orderrep.getOrderByUser(userid)
        # orders.sort(key=lambda order: order.time, reverse=True)
        foodlist = []
        for order in orders:
            foods = foodrep.getFoodByOrder(order.orderid)
            foods = [food.foodname for food in foods]
            foodlist.append(str.join(",", foods))
        while len(orders) < 3:
            orders.append(Order("", "", "", ""))
            foodlist.append("暂无")
        return orders, foodlist

    def insertOrder(self, price, address, receiver, receiver_phone, foodids):
        time = datetime.now()
        time = time.strftime("%Y-%m-%d %H:%M:%S")
        orderid = orderrep.insertOrder(time, price, address, receiver, receiver_phone)
        orderrep.insertOrderFood(orderid, foodids)
        orderrep.insertOrderUser(current_user.id, orderid)
