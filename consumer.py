import pika

connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host='172.19.60.27', port=5672,
                credentials=pika.PlainCredentials(username='shayan', password='1234')))

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