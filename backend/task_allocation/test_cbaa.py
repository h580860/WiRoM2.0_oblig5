from cbaa import CBAA
import pika
import json

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


if __name__ == '__main__':
    user_tasks0 = ["go_forward", "turn_right", "go_backwards"]
    user_tasks1 = ["go_forward", "turn_right", "turn_left"]
    user_tasks2 = ["go_forward", "turn_right", "turn_right", "turn_right", "turn_right"]
    user_tasks3 = ["go_forward"]

    tasks_list = [user_tasks0, user_tasks1, user_tasks2, user_tasks3]
    
    # test_send_fanout_message()
    send_task_list(json.dumps(tasks_list))
