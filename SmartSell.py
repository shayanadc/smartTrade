class SmartSell(object):

    def __init__(self, buy_price, profit_percent, trailing_percent, MaxBid):
        self.buy_price = buy_price
        self.profit_percent = profit_percent / 100
        self.profit_price = self.buy_price * (1 + self.profit_percent)
        self.trailing_percent = trailing_percent / 100
        self.trailing_price = 0
        self.MaxBid = MaxBid

    def sellBasedOnTrailing(self):
        if self.__isBidCrossUpProfitPrice():
            self.buy_price = self.MaxBid
            self.profit_price = self.buy_price * (1 + self.profit_percent)
            self.trailing_price = self.__sellConditionPrice(self.buy_price)
            return 'BidCrossUpProfitPrice'

        if self.__isBidCrossDownSellCondition():
            return 'BidCrossDownSellCondition'

        return 'nothing'

    def __isBidCrossUpProfitPrice(self):
        if self.MaxBid >= self.buy_price * (1 + self.profit_percent): return True

    def __sellConditionPrice(self, price):
        return price * (1 - self.trailing_percent)

    def __isBidCrossDownSellCondition(self):
        if self.MaxBid < self.__sellConditionPrice(self.buy_price): return True
        return False