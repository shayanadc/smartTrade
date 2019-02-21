class SimpleSell(object):

    def __init__(self, buy_price, benefit_percent, stop_less, Bid):
        self.buy_price = buy_price
        self.benefit_price = benefit_percent / 100
        self.stop_less = stop_less / 100
        self.Bid = Bid

    def simpleSellExistCoin(self):

        if self.__isPriceCrossUpBenefitLastBid(): return True
        if self.__isPriceCrossDownStopLessBid(): return True
        return False

    def __isPriceCrossUpBenefitLastBid(self):

        max_bid = self.Bid[0]
        if max_bid >= (self.buy_price + (self.buy_price * self.benefit_price)): return True

    def __isPriceCrossDownStopLessBid(self):

        max_bid = self.Bid[0]
        if max_bid < (self.buy_price - (self.buy_price * self.stop_less)): return True
