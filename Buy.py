class Buy(object):

    def __init__(self, BuyCondition = None):
        self.buy_condition = BuyCondition
        pass

    def MaxAskSetter(self, amount):
        self.MaxAsk = amount

    def BuyPriceSetter(self, price):
        self.buy_price = price

    def TrailingPercentSetter(self, percentage):
        self.trailing_percent = percentage / 100

    def CalcBuyCondition(self):
        self.buy_condition = self.buy_price * (1 + self.trailing_percent)

    def buyBasedOnTrailing(self):
        if(self.buy_condition is not None):
            if self.MaxAsk > self.buy_condition:
                return 'BuyOrder'

        if self.MaxAsk <= self.buy_price:
            self.buy_price = self.MaxAsk
            self.CalcBuyCondition()
            return 'AskCrossDownBuyCondition'

        return 'nothing'