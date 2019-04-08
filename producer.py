import setting
from binance.client import Client
import rabbitMQ

api_key = setting.BNCAPIK
api_secret = setting.BNCSECK

client = Client(api_key, api_secret)

producer = rabbitMQ.RabbitMQ('topic_logs','topic')

def process_message(msg):
    lastBid = msg['bids'][0]
    lastAsk = msg['asks'][0]
    producer.produce('asks.BTCUSDT.info', str(lastAsk))
    producer.produce('bids.BTCUSDT.info', str(lastBid))

from binance.websockets import BinanceSocketManager

bm = BinanceSocketManager(client)

conn_key = bm.start_depth_socket('BTCUSDT',process_message,depth=5)

bm.start()