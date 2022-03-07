import pika


class MessageSubscriber:
    def __init__(self, binding_key, exchange, callback_function=None):
        self.exchange = exchange
        self.binding_key = binding_key
        self.callback_function = callback_function

    def subscription(self):
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        channel = connection.channel()
        channel.exchange_declare(exchange=self.exchange, exchange_type='direct')

        result = channel.queue_declare(queue='', exclusive=True)
        queue_name = result.method.queue

        channel.queue_bind(exchange=self.exchange, queue=queue_name, routing_key=self.binding_key)

        channel.basic_consume(queue=queue_name, on_message_callback=self.callback_function, auto_ack=True)
        channel.start_consuming()
