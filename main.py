import pika
import time
import json
import os

time.sleep(15)


hostname = os.environ["RABBITMQ_HOST_NAME"]

connection = pika.BlockingConnection(pika.ConnectionParameters(host=hostname)) 
channel = connection.channel()

channel.queue_declare(queue='order', durable=True)

message = {
    "OrderId": "1039573832",
    "Price": 90,
    "OrderDetail": [
        {
            "OrderDetailId": "242945241",
            "Price": 30,
            "productName": "Urun ismi 1"
            },
        {
            "OrderDetailId": "394958330",
            "Price": 60,
            "productName": "Urun ismi 2"
            }
    ]
}
channel.basic_publish(exchange='',
                      routing_key='order',
                      body=json.dumps(message),
                      properties=pika.BasicProperties(
                         delivery_mode = 2,
                      ))
print(" [x] Sent %r" % message)

time.sleep(30)
print(' [*] Waiting for messages. To exit press CTRL+C')


def callback(ch, method, properties, body):
    print(" [x] Received %r" % json.loads(body))


channel.basic_qos(prefetch_count=1)
channel.basic_consume(
    'order',
    callback,
    auto_ack=True
)

channel.start_consuming()
