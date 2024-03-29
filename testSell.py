from unittest import TestCase
import Sell
import UserSellProcessorUseCase

from unittest_data_provider import data_provider


class TestSell(TestCase):
    #### simple sell exist coin if get profit or loss
    conditions = lambda: (
        ({'buy': 1000, 'profit': 10, 'stop': 950, 'bid': 1100}, 'sellOrder'),
        ({'buy': 1000, 'profit': 10, 'stop': 950, 'bid': 955}, 'nothing'),
        ({'buy': 1000, 'profit': 10, 'stop': 950, 'bid': 800}, 'sellOrder'),
    )

    @data_provider(conditions)
    def test_plan_sell_for_coins_you_already_own_with_market(self, input, expected):
        buy_price = input['buy']
        profit_percent = input['profit']
        stop_price = input['stop']
        Bid = input['bid']

        s = Sell.Sell()
        s.BuyPriceSetter(buy_price)
        s.ProfitPercentSetter(profit_percent)
        s.StopLessPriceSetter(stop_price)
        s.MaxBidSetter(Bid)
        r = s.simpleSell()

        self.assertEqual(r, expected)

    #### change price for smart sell
    conditions = lambda: (
        ({'buy': 1000, 'profit': 10, 'stop': 950, 'trailing': 1, 'bid': 1100, 'crossUpProfitTimes': 1},
         {'result': 'BidCrossUpProfitPrice', 'buyPrice': 1100, 'profitPrice': 1210, 'stopLessPrice': 950,
          'trailingPrice': 1089}),
        ({'buy': 1000, 'profit': 10, 'stop': 950, 'trailing': 2, 'bid': 1100, 'crossUpProfitTimes': 0},
         {'result': 'BidCrossUpProfitPrice', 'buyPrice': 1100, 'profitPrice': 1210, 'stopLessPrice': 950,
          'trailingPrice': 1078}),
        ({'buy': 1000, 'profit': 10, 'stop': 950, 'trailing': 10, 'bid': 890, 'crossUpProfitTimes': 0},
         {'result': 'BidCrossDownStopPrice', 'buyPrice': 1000, 'profitPrice': 1100, 'stopLessPrice': 950,
          'trailingPrice': 0}),
        ({'buy': 1000, 'profit': 10, 'stop': 950, 'trailing': 1, 'bid': 1000, 'crossUpProfitTimes': 1},
         {'result': 'nothing', 'buyPrice': 1000, 'profitPrice': 1100, 'stopLessPrice': 950, 'trailingPrice': 0}),
        ({'buy': 1000, 'profit': 10, 'stop': 950, 'trailing': 1, 'bid': 990, 'crossUpProfitTimes': 1},
         {'result': 'nothing', 'buyPrice': 1000, 'profitPrice': 1100, 'stopLessPrice': 950, 'trailingPrice': 0}),
    )

    @data_provider(conditions)
    def test_plan_sell_for_coins_you_already_own_with_trailing(self, input, expected):
        buy_price = input['buy']
        profit_percent = input['profit']
        trailing_percent = input['trailing']
        stop_less_price = input['stop']
        Bid = input['bid']
        crossUpProfitTimes = input['crossUpProfitTimes']

        s = Sell.Sell()
        s.BuyPriceSetter(buy_price)
        s.ProfitPercentSetter(profit_percent)
        s.TrailingPriceSetter(trailing_percent)
        s.StopLessPriceSetter(stop_less_price)
        s.MaxBidSetter(Bid)
        s.CrossUpTimesSetter(crossUpProfitTimes)
        r = s.sellBasedOnTrailing()

        self.assertEqual(r, expected['result'])
        self.assertEqual(s.buy_price, expected['buyPrice'])
        self.assertEqual(s.profit_price, expected['profitPrice'])
        self.assertEqual(s.stop_less_price, expected['stopLessPrice'])
        self.assertEqual(s.trailing_price, expected['trailingPrice'])

    #### test smart sell user case for one Bid
    conditions = lambda: (
        ({'user': {'name': 'shayan', 'buy_price': 1000, 'profit_percent': 10, 'stop_less_percent': 5,
                   'trailing_percent': 1, 'updated_buy_price': 1000, 'crossUpProfitTimes': 0}, 'Bid': 1100},
         {'buy_price': 1000, 'updated_buy_price': 1100, 'result': 'BidCrossUpProfitPrice', 'crossUpProfitTimes': 1,
          'stop_less_price': 950}),
        ({'user': {'name': 'shayan', 'buy_price': 1000, 'profit_percent': 10, 'stop_less_percent': 5,
                   'trailing_percent': 1, 'updated_buy_price': 1000, 'crossUpProfitTimes': 1}, 'Bid': 1010},
         {'buy_price': 1000, 'updated_buy_price': 1000, 'result': 'nothing', 'crossUpProfitTimes': 1,
          'stop_less_price': 950}),
        ({'user': {'name': 'shayan', 'buy_price': 1000, 'profit_percent': 10, 'stop_less_percent': 5,
                   'trailing_percent': 1, 'updated_buy_price': 1000, 'crossUpProfitTimes': 1}, 'Bid': 890},
         {'buy_price': 1000, 'updated_buy_price': 1000, 'result': 'sellOrder', 'crossUpProfitTimes': 1,
          'stop_less_price': 950}),
        ({'user': {'name': 'shayan', 'buy_price': 1000, 'profit_percent': 10, 'stop_less_percent': 5,
                   'trailing_percent': 1, 'updated_buy_price': 1000, 'crossUpProfitTimes': 0}, 'Bid': 890},
         {'buy_price': 1000, 'updated_buy_price': 1000, 'result': 'BidCrossDownStopPrice', 'crossUpProfitTimes': 0,
          'stop_less_price': 950, }),
    )

    @data_provider(conditions)
    def test_user_process_for_get_new_buy_price(self, input, expected):
        user = input['user']
        userObj = type('', (object,), user)()
        Bid = input['Bid']

        p = UserSellProcessorUseCase.UserSellProcessorUseCase(userObj,Bid)
        res = p.SellBasedOnTrailingForUser()
        self.assertEqual(p.user.updated_buy_price, expected['updated_buy_price'])
        self.assertEqual(p.user.buy_price, expected['buy_price'])
        self.assertEqual(p.user.crossUpProfitTimes, expected['crossUpProfitTimes'])
        self.assertEqual(p.stop_less_price, expected['stop_less_price'])
        self.assertEqual(res, expected['result'])

    # #### test user case for many Bid query

    conditions = lambda: (
        (
            {'user': {'name': 'shayan', 'buy_price': 1000, 'profit_percent': 20, 'stop_less_percent': 5,
                      'trailing_percent': 2, 'updated_buy_price': 1000, 'crossUpProfitTimes': 0},
             'Bids': [1000, 1100, 1200, 900]},
            {'results': ['nothing', 'nothing', 'BidCrossUpProfitPrice', 'sellOrder']}),
        (
            {'user': {'name': 'shayan', 'buy_price': 1000, 'profit_percent': 10, 'stop_less_percent': 5,
                      'trailing_percent': 2, 'updated_buy_price': 1000, 'crossUpProfitTimes': 0},

             'Bids': [1000, 1010, 1010, 1020, 1030, 1010, 1050, 1100, 1150, 1200, 1100, 1090, 1070]},
            {'results': ['nothing', 'nothing', 'nothing', 'nothing', 'nothing', 'nothing', 'nothing',
                         'BidCrossUpProfitPrice', 'nothing', 'nothing', 'nothing', 'nothing',
                         'sellOrder']}),
        (
            {'user': {'name': 'shayan', 'buy_price': 1000, 'profit_percent': 10, 'stop_less_percent': 5,
                      'trailing_percent': 2,
                      'updated_buy_price': 1000, 'crossUpProfitTimes': 0},
             'Bids': [1000, 1010, 1010, 1020, 1030, 1010, 1050, 1100, 1150, 1200, 1100, 1090, 1200, 1250]},
            {'results': ['nothing', 'nothing', 'nothing', 'nothing', 'nothing', 'nothing', 'nothing',
                         'BidCrossUpProfitPrice', 'nothing', 'nothing', 'nothing', 'nothing',
                         'nothing', 'BidCrossUpProfitPrice']}),

        (
            {'user': {'name': 'shayan', 'buy_price': 1000, 'profit_percent': 10, 'stop_less_percent': 5,
                      'trailing_percent': 2,
                      'updated_buy_price': 1000, 'crossUpProfitTimes': 0},
             'Bids': [1000, 1010, 1010, 1020, 1030, 1010, 1050, 1100, 1150, 1200, 1100, 1090, 1200, 1250, 1300, 1380,
                      1350]},
            {'results': ['nothing', 'nothing', 'nothing', 'nothing', 'nothing', 'nothing', 'nothing',
                         'BidCrossUpProfitPrice', 'nothing', 'nothing', 'nothing', 'nothing',
                         'nothing', 'BidCrossUpProfitPrice', 'nothing', 'BidCrossUpProfitPrice',
                         'sellOrder']}),
    )

    @data_provider(conditions)
    def test_user_process_for_many_bid_query(self, input, expected):
        Bids = input['Bids']
        user = input['user']
        userObj = type('', (object,), user)()
        results = expected['results']
        k = 0
        for i in Bids:
            p = UserSellProcessorUseCase.UserSellProcessorUseCase(userObj,i)
            res = p.SellBasedOnTrailingForUser()
            self.assertEqual(res, results[k])
            userObj = userObj
            k = k + 1