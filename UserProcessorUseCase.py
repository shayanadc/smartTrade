from  SmartSell import SmartSell

class UserProcessorUseCase(object):

    def __init__(self, user, Bid):
        self.user = user
        self.Bid = Bid
        self.stop_less_price = user.buy_price * (1 - user.stop_less_percent/100)

    def update(self):
        smartTrade = SmartSell(self.user.updated_buy_price, self.user.profit_percent, self.stop_less_price, self.user.trailing_percent,self.user.crossUpProfitTimes, self.Bid)
        s = smartTrade.sellBasedOnTrailing()
        self.user.updated_buy_price = smartTrade.buy_price
        if s == 'BidCrossUpProfitPrice' : self.user.crossUpProfitTimes = self.user.crossUpProfitTimes + 1
        return s