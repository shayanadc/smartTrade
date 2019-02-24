from unittest import TestCase
import SimpleSell
import SmartSell
import UserProcessorUseCase

from unittest_data_provider import data_provider


class TestSell(TestCase):
    #### simple sell exist coin if get profit or loss
    conditions = lambda: (
        ({'buy': 1000, 'profit': 10, 'stop': 5, 'bid': [1100, 1010, 999, 998]}, 'isPriceCrossUpProfitLastBid'),
        ({'buy': 1000, 'profit': 10, 'stop': 5, 'bid': [955, 900, 400]}, 'nothing'),
        ({'buy': 1000, 'profit': 10, 'stop': 5, 'bid': [800, 7000, 600, 500]}, 'isPriceCrossDownStopLessBid'),
    )

    @data_provider(conditions)
    def test_plan_sell_for_coins_you_already_own_with_market(self, input, expected):
        buy_price = input['buy']
        profit_percent = input['profit']
        stop_percent = input['stop']
        Bid = input['bid']

        s = SimpleSell.SimpleSell(buy_price, profit_percent, stop_percent, Bid)

        self.assertEqual(s.simpleSellOwnCoin(), expected)

    #### change price for smart sell
    conditions = lambda: (
        ({'buy': 1000, 'profit': 10, 'trailing': 1, 'bid': 1100, 'crossUpProfitTimes' : 1}, {'result':'BidCrossUpProfitPrice', 'buyPrice' : 1100, 'profitPrice' : 1210, 'trailingPrice': 1089}),
        ({'buy': 1000, 'profit': 10, 'trailing': 10, 'bid': 890,'crossUpProfitTimes' : 1}, {'result':'BidCrossDownSellCondition','buyPrice' : 1000, 'profitPrice' : 1100, 'trailingPrice': 0}),
        ({'buy': 1000, 'profit': 10, 'trailing': 10, 'bid': 890,'crossUpProfitTimes' : 0}, {'result':'nothing','buyPrice' : 1000, 'profitPrice' : 1100, 'trailingPrice': 0}),
        ({'buy': 1000, 'profit': 10, 'trailing': 1, 'bid': 1000,'crossUpProfitTimes' : 1}, {'result':'nothing','buyPrice' : 1000, 'profitPrice' : 1100, 'trailingPrice': 0}),
        ({'buy': 1000, 'profit': 10, 'trailing': 1, 'bid': 990,'crossUpProfitTimes' : 1}, {'result':'nothing','buyPrice' : 1000, 'profitPrice' : 1100, 'trailingPrice': 0}),
    )

    @data_provider(conditions)
    def test_plan_sell_for_coins_you_already_own_with_trailing(self, input, expected):
        buy_price = input['buy']
        profit_percent = input['profit']
        trailing_percent = input['trailing']
        Bid = input['bid']
        crossUpProfitTimes = input['crossUpProfitTimes']

        s = SmartSell.SmartSell(buy_price, profit_percent, trailing_percent, crossUpProfitTimes, Bid)

        self.assertEqual(s.sellBasedOnTrailing(), expected['result'])
        self.assertEqual(s.buy_price, expected['buyPrice'])
        self.assertEqual(s.profit_price, expected['profitPrice'])
        self.assertEqual(s.trailing_price, expected['trailingPrice'])

    #### test smart sell user case for one Bid
    conditions = lambda: (
        ({'user':{'name' : 'shayan' , 'buy_price' : 1000, 'profit_percent' : 10, 'trailing_percent' : 1, 'updated_buy_price': 1000,'crossUpProfitTimes' : 0}, 'Bid': 1100}, {'buy_price': 1000,'updated_buy_price' : 1100,'result': 'BidCrossUpProfitPrice','crossUpProfitTimes': 1}),
        ({'user':{'name' : 'shayan' , 'buy_price' : 1000, 'profit_percent' : 10, 'trailing_percent' : 1, 'updated_buy_price': 1000,'crossUpProfitTimes' : 1}, 'Bid': 1010}, {'buy_price': 1000,'updated_buy_price' : 1000,'result': 'nothing','crossUpProfitTimes': 1}),
        ({'user':{'name' : 'shayan' , 'buy_price' : 1000, 'profit_percent' : 10, 'trailing_percent' : 1, 'updated_buy_price': 1000,'crossUpProfitTimes' : 1}, 'Bid': 890}, {'buy_price': 1000,'updated_buy_price' : 1000,'result': 'BidCrossDownSellCondition', 'crossUpProfitTimes': 1}),
        ({'user': {'name': 'shayan', 'buy_price': 1000, 'profit_percent': 10, 'trailing_percent': 1, 'updated_buy_price': 1000, 'crossUpProfitTimes': 0}, 'Bid': 890},{'buy_price': 1000, 'updated_buy_price': 1000, 'result': 'nothing','crossUpProfitTimes': 0}),
    )

    @data_provider(conditions)
    def test_user_process_for_get_new_buy_price(self,input,expected):
        user = input['user']
        userObj = type('', (object,), user)()
        Bid = input['Bid']

        p = UserProcessorUseCase.UserProcessorUseCase(userObj, Bid)
        res = p.update()
        self.assertEqual(userObj.updated_buy_price, expected['updated_buy_price'])
        self.assertEqual(userObj.buy_price, expected['buy_price'])
        self.assertEqual(userObj.crossUpProfitTimes, expected['crossUpProfitTimes'])
        self.assertEqual(res, expected['result'])

    # #### test user case for many Bid query

    conditions = lambda: (
        ({'user': {'name':'shayan', 'buy_price' : 1000, 'profit_percent': 20, 'trailing_percent': 2, 'updated_buy_price': 1000,'crossUpProfitTimes' : 0},'Bids' : [1000,1100,1200,900]}, {'results': ['nothing', 'nothing', 'BidCrossUpProfitPrice', 'BidCrossDownSellCondition']}),
    )
    @data_provider(conditions)
    def test_user_process_for_many_bid_query(self,input,expected):
        Bids = input['Bids']
        user = input['user']
        userObj = type('', (object,), user)()
        results = expected['results']
        k = 0
        for i in Bids:
            p = UserProcessorUseCase.UserProcessorUseCase(userObj, i)
            res = p.update()
            self.assertEqual(res,results[k])
            userObj = userObj
            k = k + 1