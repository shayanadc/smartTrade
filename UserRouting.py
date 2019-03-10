import UserSellProcessorUseCase
import UserPreference
class UserRouting(object):

    def __init__(self):
        pass

    def runBid(self,BID,Pair):
        u = UserPreference.UserPreference(Pair)
        users = u.allUserForPair()
        result = None
        for user in users:
            s = UserSellProcessorUseCase.UserSellProcessorUseCase(user,BID)
            if user.tradeType == 'simpleSell':
                result = s.SimpleSellForUser()
            if user.tradeType == 'smartSell':
                result = s.SellBasedOnTrailingForUser()
        #     ##Todo: what happen if type is not defined

            import csv
            import os.path

            file_exists = os.path.isfile('trade.csv')

            toCSV = [{'name': user.name,'buy_price': s.user.buy_price, 'updated_buy_price' : s.user.updated_buy_price, 'Bid': BID, 'Pair': Pair, 'result': result}]
            with open('trade.csv', 'a', encoding='utf8', newline='') as output_file:
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

            ##csv creator
            ## user ask/bid result

