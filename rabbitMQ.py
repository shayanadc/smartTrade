import pika
import setting

class RabbitMQ:
    def __init__(self, exc_name, exc_type):
        self.exc_name = exc_name
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=setting.RABBITHOST))
        self.channel = self.connection.channel()
        self.channel.exchange_declare(exchange=self.exc_name, exchange_type=exc_type)

    def close(self):
        self.connection.close()


    def produce(self, routing_key, message):
        self.channel.basic_publish(exchange=self.exc_name, routing_key=routing_key, body=message)


    def consume(self, routing_key):

        result = self.channel.queue_declare(exclusive=True)
        self.queue_name = result.method.queue

        self.channel.queue_bind(exchange=self.exc_name,
                                queue=self.queue_name,
                                routing_key=routing_key)

        self.channel.basic_consume(self.callback,
                                   queue=self.queue_name,
                                   no_ack=False)

        self.channel.start_consuming()

    def callback(self,ch, method, properties, body):
        symbol = method.routing_key.split('.')
        type = symbol[0]
        pair = symbol[1]
        body = body.decode('utf8').replace("'", '"')
        import json
        body = json.loads(body)
        import UserRouting
        r = UserRouting.UserRouting()
        if type == 'bids':
            bid = body[0]
            latestBid = float(bid)
            result = r.runBid(latestBid, pair)
        if type == 'asks':
            ask = body[0]
            latestAsk = float(ask)
            result = r.runAsk(latestAsk, pair)

        ch.basic_ack(delivery_tag=method.delivery_tag)

