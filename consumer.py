import rabbitMQ
producer = rabbitMQ.RabbitMQ('topic_logs','topic')
producer.consume('#')