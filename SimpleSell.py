class SimpleSell(object):

    def __init__(self, buy_price, profit_percent, stop_less, Bid):
        self.buy_price = buy_price
        self.profit_price = profit_percent / 100
        self.stop_less = stop_less / 100
        self.Bid = Bid

    def simpleSellOwnCoin(self):

        if self.__isPriceCrossUpProfitLastBid(): return 'isPriceCrossUpProfitLastBid'
        if self.__isPriceCrossDownStopLessBid(): return 'isPriceCrossDownStopLessBid'
        return 'nothing'

    def __isPriceCrossUpProfitLastBid(self):

        max_bid = self.Bid[0]
        if max_bid >= (self.buy_price + (self.buy_price * self.profit_price)): return 'isPriceCrossUpProfitLastBid'

    def __isPriceCrossDownStopLessBid(self):

        max_bid = self.Bid[0]
        if max_bid < (self.buy_price - (self.buy_price * self.stop_less)): return 'isPriceCrossDownStopLessBid'
