from unittest import TestCase
from unittest_data_provider import data_provider
import Buy
import UserBuyProcessorUseCase


class TestBuy(TestCase):
    conditions = lambda: (
        ({'buy_price': 1000, 'trailing': 2, 'ask': 999}, {'result' : 'AskCrossUpBuyCondition', 'buy_price' : 999, 'buy_condition' : 1018.98}),
        ({'buy_price': 1000, 'trailing': 2, 'ask': 990, 'buy_condition': 980}, {'result' : 'BuyOrder', 'buy_price' : 1000,'buy_condition' : 980}),
        ({'buy_price': 1000, 'trailing': 2, 'ask': 1100}, {'result' : 'nothing', 'buy_price' : 1000, 'buy_condition': None}),
        ({'buy_price': 1000, 'trailing': 2, 'ask': 1010, 'buy_condition' : 1020}, {'result' : 'nothing', 'buy_price' : 1000, 'buy_condition': 1020}),
    )

    @data_provider(conditions)
    def test_plan_sell_for_coins_you_already_own_with_market(self, input, expected):

        buy_condition = None
        buy_price = input['buy_price']
        trailing_percent = input['trailing']
        if('buy_condition' in input): buy_condition = input['buy_condition']

        Ask = input['ask']

        s = Buy.Buy(buy_condition)
        s.BuyPriceSetter(buy_price)
        s.MaxAskSetter(Ask)
        s.TrailingPercentSetter(trailing_percent)

        r = s.buyBasedOnTrailing()

        self.assertEqual(r, expected['result'])
        self.assertEqual(s.buy_price, expected['buy_price'])
        self.assertEqual(s.buy_condition, expected['buy_condition'])

    conditions = lambda: (
            ({'user': {'name': 'shayan', 'buy_price': 1000,'updated_buy_price' : 1000,'trailing_percent': 2}, 'Ask': 999},{'buy_price': 1000, 'updated_buy_price': 999, 'result': 'AskCrossUpBuyCondition'}),
            ({'user': {'name': 'shayan', 'buy_price': 1000,'updated_buy_price' : 1000,'trailing_percent': 2,'buy_condition': 980}, 'Ask': 999},{'buy_price': 1000, 'updated_buy_price': 1000, 'result': 'BuyOrder'}),
            ({'user': {'name': 'shayan', 'buy_price': 1000,'updated_buy_price' : 1000,'trailing_percent': 2}, 'Ask': 1100},{'buy_price': 1000, 'updated_buy_price': 1000, 'result': 'nothing'}),
        )

    @data_provider(conditions)
    def test_buy_with_trailing_price(self, input, expected):
        user = input['user']
        userObj = type('', (object,), user)()
        Ask = input['Ask']

        p = UserBuyProcessorUseCase.UserBuyProcessorUseCase(userObj)
        p.MaxAskSetter(Ask)
        res = p.BuyBasedOnTrailingForUser()
        self.assertEqual(res, expected['result'])
        self.assertEqual(userObj.updated_buy_price, expected['updated_buy_price'])
        self.assertEqual(userObj.buy_price, expected['buy_price'])