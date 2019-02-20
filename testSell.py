from unittest import TestCase
from unittest.mock import Mock
import Sell
from unittest_data_provider import data_provider

class TestSell(TestCase):
    colors = lambda: (
        ({'buy' :1000, 'benefit': 10, 'stop' : 5, 'bid' : [1100,1010,999,998]}, True),
        ({'buy' :1000, 'benefit': 10, 'stop' : 5 , 'bid' : [955,900,400]}, False),
        ({'buy' :1000, 'benefit': 10, 'stop' : 5, 'bid' : [800,7000,600,500]}, True),
    )
    @data_provider(colors)
    def test_plan_sell_for_coins_you_already_own_with_market(self,input,expected):

        buy_price = input['buy']
        benefit_percent = input['benefit']
        stop_percent = input['stop']
        Bid = input['bid']

        s = Sell.Sell(buy_price,benefit_percent, stop_percent,Bid)

        self.assertEqual(s.sellOrder(), expected)