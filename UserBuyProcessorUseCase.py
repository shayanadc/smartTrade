from Buy import Buy
class UserBuyProcessorUseCase(object):

    def __init__(self, user):
        self.user = user
    def MaxAskSetter(self, MaxAskAmount):
        self.MaxAsk = MaxAskAmount

    def BuyBasedOnTrailingForUser(self):
        smartTrade = Buy(self.user.buy_condition)
        smartTrade.MaxAskSetter(self.MaxAsk)
        smartTrade.BuyPriceSetter(self.user.updated_buy_price)
        smartTrade.TrailingPercentSetter(self.user.trailing_percent)
        r = smartTrade.buyBasedOnTrailing()
        self.user.updated_buy_price = smartTrade.buy_price
        self.user.buy_condition = smartTrade.buy_condition
        return r
