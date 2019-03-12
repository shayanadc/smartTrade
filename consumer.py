import pika
import setting
import time
try:
    connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=setting.RABBITHOST, port=setting.RABBITPORT,
                credentials=pika.PlainCredentials(username=setting.RABBITUSERNAME, password=setting.RABBITPASS)))
except Exception as e:
    time.sleep(60)
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host=setting.RABBITHOST, port=setting.RABBITPORT,
            credentials=pika.PlainCredentials(username=setting.RABBITUSERNAME, password=setting.RABBITPASS)))

channel = connection.channel()

channel.queue_declare(queue='price',passive=True,auto_delete=False,durable=False,exclusive=False)

def callback(ch, method, properties, body):
    body = body.decode('utf8').replace("'", '"')
    import json
    body = json.loads(body)
    import UserRouting
    r = UserRouting.UserRouting()
    bid = body['bid']
    latestBid = float(bid)
    result = r.runBid(latestBid,body['symbol'])
    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(callback,
                      queue='price')

channel.start_consuming()