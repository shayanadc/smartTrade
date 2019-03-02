from Buy import Buy
class UserBuyProcessorUseCase(object):

    def __init__(self, user):
        self.user = user
        self.buy_condition = None
        if hasattr(user, 'buy_condition'): self.buy_condition = user.buy_condition

    def MaxAskSetter(self, MaxAskAmount):
        self.MaxAsk = MaxAskAmount

    def BuyBasedOnTrailingForUser(self):
        smartTrade = Buy(self.buy_condition)
        smartTrade.MaxAskSetter(self.MaxAsk)
        smartTrade.BuyPriceSetter(self.user.updated_buy_price)
        smartTrade.TrailingPercentSetter(self.user.trailing_percent)
        r = smartTrade.buyBasedOnTrailing()
        self.user.updated_buy_price = smartTrade.buy_price
        return r
