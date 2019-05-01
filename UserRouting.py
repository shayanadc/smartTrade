import UserSellProcessorUseCase
import UserBuyProcessorUseCase
import UserPreference
import setting
class UserRouting(object):

    def __init__(self):
        pass

    def runAsk(self,Ask,Pair):
        u = UserPreference.UserPreference(Pair)
        users = u.allUserForBuyPair()

        result = None
        for user in users:
            s = UserBuyProcessorUseCase.UserBuyProcessorUseCase(user, Ask)
            if user.tradeType == 'smartBuy':
                result = s.BuyBasedOnTrailingForUser()

            import csv
            import os.path


            toCSV = [{'name': user.name, 'buy_price': s.user.buy_price,
                      'updated_buy_price': s.user.updated_buy_price,
                      'Ask': Ask, 'Pair': Pair, 'result': result}]
            fileaddr = setting.REPORT_ADDR + 'trade_buy.csv'
            file_exists = os.path.isfile(fileaddr)
            with open(fileaddr, 'a', encoding='utf8', newline='') as output_file:
                fc = csv.DictWriter(output_file,
                                    fieldnames=toCSV[0].keys(),
                                    )
                if not file_exists:
                    fc.writeheader()
                fc.writerows(toCSV)

            if result == 'BuyOrder':
                u.changeUserType(s.user,Ask)

            if result == 'AskCrossDownBuyCondition':
                u.updateUser(s.user)

    def runBid(self,BID,Pair):
        u = UserPreference.UserPreference(Pair)
        users = u.allUserForSellPair()
        result = None
        for user in users:
            s = UserSellProcessorUseCase.UserSellProcessorUseCase(user,BID)
            if user.tradeType == 'simpleSell':
                result = s.SimpleSellForUser()
            if user.tradeType == 'smartSell':
                result = s.SellBasedOnTrailingForUser()

            import csv
            import os.path


            toCSV = [{'name': user.name,'buy_price': s.user.buy_price, 'updated_buy_price' : s.user.updated_buy_price, 'Bid': BID, 'Pair': Pair, 'result': result}]

            fileaddr = setting.REPORT_ADDR + 'trade_sell.csv'
            file_exists = os.path.isfile(fileaddr)

            with open(fileaddr, 'a', encoding='utf8', newline='') as output_file:
                fc = csv.DictWriter(output_file,
                                    fieldnames=toCSV[0].keys(),
                                    )
                if not file_exists:
                    fc.writeheader()
                fc.writerows(toCSV)


            if result == 'sellOrder':
                u.deleteUser(s.user)
            if result == 'BidCrossDownStopPrice' or result == 'BidCrossUpProfitPrice':
                u.updateUser(s.user)