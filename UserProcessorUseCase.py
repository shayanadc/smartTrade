from  SmartSell import SmartSell

class UserProcessorUseCase(object):

    def __init__(self, user, Bid):
        self.user = user
        self.Bid = Bid

    def update(self):
        smartTrade = SmartSell(self.user.updated_buy_price, self.user.profit_percent, self.user.trailing_percent, self.Bid)
        s = smartTrade.sellBasedOnTrailing()
        self.user.updated_buy_price = smartTrade.buy_price
        return s