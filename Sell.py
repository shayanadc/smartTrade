class Sell(object):

    def __init__(self):
        self.trailing_price = 0
        pass

    def MaxBidSetter(self, amount):
        self.MaxBid = amount

    def BuyPriceSetter(self, price):
        self.buy_price = price

    def ProfitPercentSetter(self, percentage):
        self.profit_percent = percentage / 100
        self.profitPriceCalc()

    def profitPriceCalc(self):
        self.profit_price = self.buy_price * (1 + self.profit_percent)

    def StopLessPriceSetter(self, price):
        self.stop_less_price = price

    def CrossUpTimesSetter(self, times):
        self.crossUpProfitTimes = times

    def TrailingPriceSetter(self, percentage):
        self.trailing_percent = percentage / 100

    def sellBasedOnTrailing(self):
        if self.__isBidCrossUpProfitPrice():
            self.buy_price = self.MaxBid
            self.profitPriceCalc()
            self.trailing_price = self.__sellConditionPrice()
            return 'BidCrossUpProfitPrice'

        if self.__isBidCrossDownSellCondition() and self.crossUpProfitTimes >= 1:
            return 'sellOrder'

        if self.__isBidCrossDownStopPrice():
            return 'BidCrossDownStopPrice'

        return 'nothing'

    def simpleSell(self):
        if self.__isBidCrossUpProfitPrice(): return 'sellOrder'
        if self.__isBidCrossDownStopPrice(): return 'sellOrder'
        return 'nothing'

    def __isBidCrossDownStopPrice(self):
        if self.MaxBid < self.stop_less_price: return True

    def __isBidCrossUpProfitPrice(self):
        if self.MaxBid >= self.profit_price: return True

    def __sellConditionPrice(self):
        return self.buy_price * (1 - self.trailing_percent)

    def __isBidCrossDownSellCondition(self):
        if self.MaxBid < self.__sellConditionPrice(): return True
        return False