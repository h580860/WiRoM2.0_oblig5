import pika


class MessageSubscriber:
    def __init__(self, binding_key, exchange, exchange_type, callback_function=None):
        self.exchange = exchange
        self.binding_key = binding_key
        self.callback_function = callback_function
        self.exchange_type = exchange_type

    def subscription(self):
        # NOTE! heartbeat interval is disabled. This is bad practice, but is done so RabbitMQ does not cancel the 
        # connection. 
        # See GitHub issue: 
        # https://github.com/pika/pika/issues/1224
        # Disabled by doing: https://github.com/pika/pika/blob/1.0.1/pika/connection.py#L554
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', heartbeat=0))
        channel = connection.channel()
        channel.exchange_declare(exchange=self.exchange, exchange_type=self.exchange_type)

        result = channel.queue_declare(queue='', exclusive=True)
        queue_name = result.method.queue

        channel.queue_bind(exchange=self.exchange, queue=queue_name, routing_key=self.binding_key)

        channel.basic_consume(queue=queue_name, on_message_callback=self.callback_function, auto_ack=True)
        channel.start_consuming()
