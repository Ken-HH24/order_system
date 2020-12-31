# from config import cursor
import DAO.Database as Database
import traceback


def start_transaction(origin_func):
    def wrapper(self, *args, **kwargs):
        try:
            self.conn, self.cursor = Database.getConnect()
            u = origin_func(self, *args, **kwargs)
            return u
        except Exception:
            self.conn.rollback()  # 事务回滚
            return 'an Exception raised.'
        finally:
            Database.closeConnect(self.conn)
    return wrapper


class Food:
    def __init__(self, foodid, foodname, price, sales, type):
        self.foodid = foodid
        self.foodname = foodname
        self.price = price
        self.sales = sales
        self.type = type


class FoodRepository:
    def __init__(self):
        self.conn = None
        self.cursor = None

    def __packFood(self, foods):
        ans = []
        for item in foods:
            ans.append(Food(item['foodid'], item['foodname'], item['price'], item['sales'], item['type']))
        return ans

    @start_transaction
    def getAllFood(self):
        sql = "SELECT * FROM Food"
        self.cursor.execute(sql)
        res = self.cursor.fetchall()
        return self.__packFood(res)

    @start_transaction
    def getFoodByType(self, type):
        sql = "SELECT * FROM Food WHERE type = %s"
        self.cursor.execute(sql, type)
        res = self.cursor.fetchall()
        return self.__packFood(res)

    @start_transaction
    def getFoodByOrder(self, orderid):
        sql = "SELECT * FROM Food LEFT JOIN order_food ON Food.foodid = order_food.foodid " \
              "WHERE orderid = %s"  # join查询 参照完整性约束
        # sql = "SELECT * FROM Food WHERE foodid in " \
        #       "(SELECT foodid FROM order_food WHERE orderid = %s)"
        self.cursor.execute(sql, orderid)
        res = self.cursor.fetchall()
        return self.__packFood(res)

    @start_transaction
    def getTopSailFood(self, num=3):
        sql = "SELECT foodname, sales FROM v_popfood ORDER BY sales DESC LIMIT %s"
        self.cursor.execute(sql, num)
        res = self.cursor.fetchall()
        ans = []
        for item in res:
            ans.append({'foodname': item['foodname'], 'sales': item['sales']})
        return ans

    @start_transaction
    def getFoodType(self):
        sql = "SELECT DISTINCT type FROM food"
        self.cursor.execute(sql)
        res = self.cursor.fetchall()
        ans = [t['type'] for t in res]
        return ans

    @start_transaction
    def getPrice(self, *ids):
        concat = ",".join(["%s" for i in range(len(*ids))])
        sql = "SELECT SUM(price) AS sum FROM food WHERE foodid in (" + concat + ")"
        self.cursor.execute(sql, *ids)
        res = self.cursor.fetchone()['sum']
        return res
