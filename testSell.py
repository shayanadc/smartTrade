from unittest import TestCase
import SimpleSell
import SmartSell
from unittest_data_provider import data_provider


class TestSell(TestCase):
    conditions = lambda: (
        ({'buy': 1000, 'benefit': 10, 'stop': 5, 'bid': [1100, 1010, 999, 998]}, True),
        ({'buy': 1000, 'benefit': 10, 'stop': 5, 'bid': [955, 900, 400]}, False),
        ({'buy': 1000, 'benefit': 10, 'stop': 5, 'bid': [800, 7000, 600, 500]}, True),
    )

    @data_provider(conditions)
    def test_plan_sell_for_coins_you_already_own_with_market(self, input, expected):
        buy_price = input['buy']
        benefit_percent = input['benefit']
        stop_percent = input['stop']
        Bid = input['bid']

        s = SimpleSell.SimpleSell(buy_price, benefit_percent, stop_percent, Bid)

        self.assertEqual(s.simpleSellExistCoin(), expected)

    conditions = lambda: (
        ({'buy': 1000, 'benefit': 10, 'trailing': 1, 'bid': 1100}, [1100, 1210, 1089]),
        ({'buy': 1000, 'benefit': 10, 'trailing': 1, 'bid': 955}, [1000, 1100]),
        ({'buy': 1000, 'benefit': 10, 'trailing': 1, 'bid': 800}, [1000, 1100]),
    )

    @data_provider(conditions)
    def test_plan_sell_for_coins_you_already_own_with_trailing(self, input, expected):
        buy_price = input['buy']
        benefit_percent = input['benefit']
        trailing_percent = input['trailing']
        Bid = input['bid']

        s = SmartSell.SmartSell(buy_price, benefit_percent, trailing_percent, Bid)
        self.assertEqual(s.trailingSell(), expected)

    conditions = lambda: (
        ({'buy': 1000, 'benefit': 10, 'trailing': 10, 'bid': 890}, True),
        ({'buy': 1000, 'benefit': 10, 'trailing': 10, 'bid': 955}, False),
        ({'buy': 1000, 'benefit': 10, 'trailing': 10, 'bid': 900}, False),
    )

    @data_provider(conditions)
    def test_sell_if_trailing_cross_down(self, input, expected):
        buy_price = input['buy']
        benefit_percent = input['benefit']
        trailing_percent = input['trailing']
        Bid = input['bid']

        s = SmartSell.SmartSell(buy_price, benefit_percent, trailing_percent, Bid)
        self.assertEqual(s.BidCrossDownSellCondition(), expected)
