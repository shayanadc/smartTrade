from Sell import Sell

class UserProcessorUseCase(object):

    def __init__(self, user):
        self.user = user
        self.stop_less_price = user.buy_price * (1 - user.stop_less_percent / 100)

    def MaxBidSetter(self,MaxBidAmount):
        self.MaxBid = MaxBidAmount

    def SimpleSellForUser(self):
        smartTrade = Sell()
        smartTrade.MaxBidSetter(self.MaxBid)
        smartTrade.BuyPriceSetter(self.user.buy_price)
        smartTrade.ProfitPercentSetter(self.user.profit_percent)
        smartTrade.StopLessPriceSetter(self.stop_less_price)
        return smartTrade.simpleSell()

    def SellBasedOnTrailingForUser(self):
        smartTrade = Sell()
        smartTrade.MaxBidSetter(self.MaxBid)
        smartTrade.BuyPriceSetter(self.user.updated_buy_price)
        smartTrade.ProfitPercentSetter(self.user.profit_percent)
        smartTrade.StopLessPriceSetter(self.stop_less_price)
        smartTrade.TrailingPriceSetter(self.user.trailing_percent)
        smartTrade.CrossUpTimesSetter(self.user.crossUpProfitTimes)

        s = smartTrade.sellBasedOnTrailing()
        self.user.updated_buy_price = smartTrade.buy_price
        if s == 'BidCrossUpProfitPrice': self.user.crossUpProfitTimes += 1
        return s