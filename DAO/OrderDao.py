# from config import cursor, conn
import DAO.Database as Database


def start_transaction(origin_func):
    def wrapper(self, *args, **kwargs):
        try:
            self.conn, self.cursor = Database.getConnect()
            u = origin_func(self, *args, **kwargs)
            return u
        except Exception as error:
            self.conn.rollback()  # 事务回滚
            return 'an Exception raised.'
        finally:
            Database.closeConnect(self.conn)

    return wrapper


class Order(object):
    def __init__(self, orderid, price, time, address):
        self.orderid = orderid
        self.price = price
        self.time = time
        self.address = address


class OrderRepository:
    def __init__(self):
        self.conn = None
        self.cursor = None

    def __packOrder(self, orders):
        ans = []
        for order in orders:
            ans.append(Order(order['orderid'], order['price'], order['TIME'], order['address']))
        return ans

    @start_transaction
    def getAllOrder(self):
        sql = "SELECT * FROM orders"
        self.cursor.execute(sql)
        res = self.cursor.fetchall()
        return self.__packOrder(res)

    @start_transaction
    def getOrderByUser(self, userid):
        sql = "SELECT * FROM orders WHERE orderid in " \
              "(SELECT orderid From user_order WHERE userid = %s)" \
              "ORDER BY time DESC"  # 利用索引提高查询速度
        self.cursor.execute(sql, userid)
        res = self.cursor.fetchall()
        return self.__packOrder(res)

    @start_transaction
    def insertOrder(self, time, price, address, receiver, receiver_phone):
        sql = "INSERT INTO orders(TIME, price, address, receiver, receiver_phone) VALUES (%s, %s, %s, %s, %s)"
        self.cursor.execute(sql, (time, float(price), address, receiver, receiver_phone))
        orderid = self.cursor.lastrowid  # 获取自增id
        self.conn.commit()
        return orderid

    @start_transaction
    def insertOrderFood(self, orderid, foodids):
        sql = "INSERT INTO order_food(orderid, foodid) VALUES (%s, %s)"
        for foodid in foodids:
            self.cursor.execute(sql, (orderid, foodid))
        self.conn.commit()

    @start_transaction
    def insertOrderUser(self, userid, orderid):
        sql = "INSERT INTO user_order(userid, orderid) VALUES (%s, %s)"
        self.cursor.execute(sql, (userid, orderid))
        self.conn.commit()
