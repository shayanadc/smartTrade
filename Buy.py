class Buy(object):

    def __init__(self):
        self.trailing_price = 0
        pass

    def MaxAskSetter(self, amount):
        self.MaxAsk = amount

    def BuyPriceSetter(self, price):
        self.buy_price = price

    def BuyConditionPriceSetter(self, price):
        self.buy_condition = price

    def TrailingPriceSetter(self, percentage):
        self.trailing_percent = percentage / 100

    def buyBasedOnTrailing(self):
        if self.MaxAsk > self.buy_condition:
                return 'BuyOrder'

        if self.MaxAsk <= self.buy_price:
            self.buy_price = self.MaxAsk
            self.buy_condition = self.buy_price * (1 + self.trailing_percent)
            return 'AskCrossUpBuyCondition'

        return 'nothing'