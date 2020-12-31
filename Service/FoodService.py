from DAO.FoodRepository import Food, FoodRepository

foodrep = FoodRepository()


class FoodService:
    def getTopSailing(self, num=3):
        foods = foodrep.getTopSailFood(num)
        ans = []
        for i in range(num):
            ans.append(foods[i])
        return ans

    def getFoodByType(self):
        foods = foodrep.getAllFood()
        res = []
        mp = {}
        for food in foods:
            if food.type not in mp:
                mp[food.type] = [food]
            else:
                mp[food.type].append(food)
        for v in mp.values():
            res.append(v)
        return res

    def getFoodType(self):
        return foodrep.getFoodType()

    def calPrice(self, *ids):
        return foodrep.getPrice(*ids)