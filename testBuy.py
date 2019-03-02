from unittest import TestCase
from unittest_data_provider import data_provider
import Buy

class TestBuy(TestCase):
    conditions = lambda: (
        ({'buy_price': 1000, 'trailing': 2, 'ask': 999,'buy_condition': 999999999}, {'result' : 'AskCrossUpBuyCondition', 'buy_price' : 999, 'buy_condition' : 1018.98}),
        ({'buy_price': 1000, 'trailing': 2, 'ask': 990, 'buy_condition': 980}, {'result' : 'BuyOrder', 'buy_price' : 1000,'buy_condition' : 980}),
        ({'buy_price': 1000, 'trailing': 2, 'ask': 1100, 'buy_condition' : 99999999}, {'result' : 'nothing', 'buy_price' : 1000, 'buy_condition': 99999999}),
        ({'buy_price': 1000, 'trailing': 2, 'ask': 1010, 'buy_condition' : 1020}, {'result' : 'nothing', 'buy_price' : 1000, 'buy_condition': 1020}),
    )

    @data_provider(conditions)
    def test_plan_sell_for_coins_you_already_own_with_market(self, input, expected):

        buy_price = input['buy_price']
        trailing_percent = input['trailing']
        buy_condition = input['buy_condition']
        Ask = input['ask']

        s = Buy.Buy()
        s.BuyPriceSetter(buy_price)
        s.MaxAskSetter(Ask)
        s.BuyConditionPriceSetter(buy_condition)
        s.TrailingPriceSetter(trailing_percent)

        r = s.buyBasedOnTrailing()

        self.assertEqual(r, expected['result'])
        self.assertEqual(s.buy_price, expected['buy_price'])
        self.assertEqual(s.buy_condition, expected['buy_condition'])