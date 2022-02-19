import pika
import time

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='topic_exchange', exchange_type='topic')

message = "sent only moose.location"
routing_key = "moose.location"
channel.basic_publish(
    exchange='topic_exchange', routing_key=routing_key, body=message)
print(" [x] Sent %r:%r" % (routing_key, message))

time.sleep(3)

message = "sent only mavic2pro"
routing_key = "mavic2pro."
channel.basic_publish(
    exchange='topic_exchange', routing_key=routing_key, body=message)
print(" [x] Sent %r:%r" % (routing_key, message))

connection.close()