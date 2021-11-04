import pika
import sys

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.exchange_declare(
    exchange='routing_exchange', exchange_type='direct')

test_moose_message = "go_forward(5),turn_right(3)"
test_mavic_message = "set_altitude(2),go_forward(3),turn_right(3)"

# publish the moose message
channel.basic_publish(exchange='routing_exchange', routing_key='moose_queue', body=test_moose_message)
print("[send_routing_message] published to moose")

# publish the mavic message
channel.basic_publish(exchange='routing_exchange', routing_key='mavic_queue', body=test_mavic_message)
print("[send_routing_message] published to mavic2pro")

connection.close()