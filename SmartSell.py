class SmartSell(object):

    def __init__(self, buy_price, profit_percent, stop_less_price, trailing_percent, crossUpProfitTimes, MaxBid):
        self.buy_price = buy_price
        self.profit_percent = profit_percent / 100
        self.profit_price = self.buy_price * (1 + self.profit_percent)
        self.stop_less_price = stop_less_price
        self.trailing_percent = trailing_percent / 100
        self.trailing_price = 0
        self.MaxBid = MaxBid
        self.crossUpProfitTimes = crossUpProfitTimes
        self.lastCrossUpProfitTimes = crossUpProfitTimes

    def sellBasedOnTrailing(self):
        if self.__isBidCrossUpProfitPrice():
            self.buy_price = self.MaxBid
            self.profit_price = self.buy_price * (1 + self.profit_percent)
            self.trailing_price = self.__sellConditionPrice(self.buy_price)
            return 'BidCrossUpProfitPrice'

        if self.__isBidCrossDownSellCondition() and self.lastCrossUpProfitTimes >= 1:
            return 'BidCrossDownSellCondition'

        if self.__isBidCrossDownStopPrice():
            return 'BidCrossDownStopPrice'

        return 'nothing'

    def __isBidCrossDownStopPrice(self):
        if self.MaxBid < self.stop_less_price: return True

    def __isBidCrossUpProfitPrice(self):
        if self.MaxBid >= self.buy_price * (1 + self.profit_percent): return True

    def __sellConditionPrice(self, price):
        return price * (1 - self.trailing_percent)

    def __isBidCrossDownSellCondition(self):
        if self.MaxBid < self.__sellConditionPrice(self.buy_price): return True
        return False