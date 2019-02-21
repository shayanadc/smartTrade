class SmartSell(object):

    def __init__(self, buy_price, benefit_percent, trailing, MaxBid):
        self.buy_price = buy_price
        self.benefit_price = benefit_percent / 100
        self.trailing = trailing / 100
        self.MaxBid = MaxBid

    def trailingSell(self):

        if self.__isBidGreaterThanBenefitPrice():
            buy_price = self.MaxBid
            return [buy_price, buy_price * (1 + self.benefit_price), self.__sellConditionPrice(buy_price)]

        return [self.buy_price, self.buy_price * (1 + self.benefit_price)]

    def __isBidGreaterThanBenefitPrice(self):
        if self.MaxBid >= self.buy_price * (1 + self.benefit_price): return True

    def __sellConditionPrice(self, price):
        return price * (1 - self.trailing)

    def BidCrossDownSellCondition(self):
        if self.MaxBid < self.__sellConditionPrice(self.buy_price): return True
        return False