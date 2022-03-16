from cbaa import CBAA
import pika
import json
import threading
from multiprocessing import Process


def test_send_fanout_message():
    print("Testing sending a message to the CBAA exchange")
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.exchange_declare(exchange='cbaa_initiate_exchange', exchange_type='fanout')

    message = "request CBAA initiation"
    channel.basic_publish(exchange='cbaa_initiate_exchange', routing_key='', body=message)
    print(" [x] Sent %r" % message)
    connection.close()


def send_task_list(task_list_as_json):
    print("Sending the task list to the robots")
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.exchange_declare(exchange='cbaa_initiate_exchange', exchange_type='fanout')

    channel.basic_publish(exchange='cbaa_initiate_exchange', routing_key='', body=task_list_as_json)
    connection.close()


def receive_result_callback(ch, method, properties, body):
    print(f"test_cbaa received {body}")


def receive_result_subscription():
    print("Waiting for results")
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    exchange_name = 'routing_exchange'
    binding_key = 'test_cbaa_routing_key'
    channel.exchange_declare(exchange=exchange_name, exchange_type='direct')

    result = channel.queue_declare(queue='', exclusive=True)
    queue_name = result.method.queue

    channel.queue_bind(exchange=exchange_name, queue=queue_name, routing_key=binding_key)

    channel.basic_consume(queue=queue_name, on_message_callback=receive_result_callback, auto_ack=True)
    channel.start_consuming()


if __name__ == '__main__':
    user_tasks0 = ["go_forward", "turn_right", "go_backwards"]
    user_tasks1 = ["go_forward", "turn_right", "turn_left"]
    user_tasks2 = ["go_forward", "turn_right", "turn_right", "turn_right", "turn_right"]
    user_tasks3 = ["go_forward"]

    formatted = [
        {"name": "task0", "simpleactions": user_tasks0},
        {"name": "task1", "simpleactions": user_tasks1},
        {"name": "task2", "simpleactions": user_tasks2},
        {"name": "task3", "simpleactions": user_tasks3},
    ]
    tasks_list = [user_tasks0, user_tasks1, user_tasks2, user_tasks3]

    # cbaa_results_communication = threading.Thread(target=receive_result_subscription)
    # cbaa_results_communication.start()

    # test_send_fanout_message()
    # send_task_list(json.dumps(tasks_list))
    send_task_list(json.dumps(formatted))

    # p = Process(target=receive_result_subscription)
    # p.start()
    # receive_result_subscription()
