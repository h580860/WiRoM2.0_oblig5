import pika
import threading


class TopicMessenger:
    """
    This class was an attempt to create a proper topic based messaging broker, however
    it does not currencly work as expected
    """
    def __init__(self, binding_key, callback_function):
        self.exchange_name = 'topic_exchange'
        self.binding_key = binding_key
        self.callback_function = callback_function

    def subscription(self):
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        channel = connection.channel()
        channel.exchange_declare(exchange=self.exchange_name, exchange_type='topic')

        result = channel.queue_declare(queue='', exclusive=True)
        queue_name = result.method.queue

        channel.queue_bind(exchange=self.exchange_name, queue=queue_name, routing_key=self.binding_key)
        # channel.queue_bind(exchange=self.exchange_name, queue=queue_name, routing_key="robotname.#")
        #channel.basic_consume(queue=queue_name, on_message_callback=self.class_callback_function, auto_ack=True)
        channel.basic_consume(queue=queue_name, on_message_callback=self.callback_function, auto_ack=True)

        print(f"Subscription with binding key: {self.binding_key} is consuming")
        channel.start_consuming()

def test_callback_function(ch, method, properties, body):
    print("Test callback function")
    print(f"ch: {ch}")
    print(f"method: {method}")
    print(f"properties: {properties}")
    print(f"body: {body}")


def subscription1():
    binding_key_with_location = "moose.location"
    topicmessenger1 = TopicMessenger(binding_key_with_location, test_callback_function)
    topicmessenger1.subscription()


def subscription2():
    binding_key_robot_only = "mavic2pro."
    topicmessenger2 = TopicMessenger(binding_key_robot_only, test_callback_function)
    topicmessenger2.subscription()


if __name__ == '__main__':
    # messenger1 = threading.Thread(target=subscription1)
    # messenger2 = threading.Thread(target=subscription2)
    #
    # messenger1.start()
    # messenger2.start()
    subscription1()
