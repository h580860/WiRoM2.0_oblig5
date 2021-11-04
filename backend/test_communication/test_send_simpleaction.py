import pika
import sys

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='test_exchange', exchange_type='fanout')

message = "go_forward(3),turn_left(3),go_backward(3)"
channel.basic_publish(exchange='test_exchange', routing_key='', body=message)
print(" [test_send_simpleaction] Sent %r" % message)
connection.close()