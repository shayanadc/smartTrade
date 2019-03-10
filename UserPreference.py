import MongoDB
class UserPreference(object):

    def __init__(self,Pair):
        self.storage = MongoDB.MongoDB(Pair)

    def savePreference(self, name, tradeType, BuyPrice, Profit, StopLess, Trailing=0, CrossUpProfitTimes=0, BuyCondition=None, UpdatedBuyPrice = None):
        if UpdatedBuyPrice is None : UpdatedBuyPrice = BuyPrice
        dict = {'name': name, 'tradeType' : tradeType, 'buy_price' :BuyPrice, 'profit_percent' : Profit, 'stop_less_percent' : StopLess, 'trailing_percent': Trailing, 'crossUpProfitTimes' : CrossUpProfitTimes, 'buy_condition': BuyCondition, 'updated_buy_price' : UpdatedBuyPrice}
        self.storage.insert(dict)

    def allUserForPair(self):
        userDict  = self.storage.findAll()
        New = []
        for i in userDict:
            i.pop("_id")
            userObj = type('', (object,), i)()
            New.append(userObj)
        return New

    def deleteUser(self,user):
        q = {'name' : user.name}
        return self.storage.delete(q)

    def updateUser(self, user):
        if hasattr(user, 'crossUpProfitTimes'): self.storage.update({'name' : user.name}, {'crossUpProfitTimes' : user.crossUpProfitTimes})
        if hasattr(user, 'buy_condition'): self.storage.update({'user': user.name}, {'buy_condition' : user.buy_condition})
        if hasattr(user, 'updated_buy_price'): self.storage.update({'name': user.name}, {'updated_buy_price' : user.updated_buy_price})