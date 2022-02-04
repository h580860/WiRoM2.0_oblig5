from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import json
import time
import logging
# from wirom_logger import Wirom_logger
# from Logs.wirom_logger import Wirom_logger
import pika
import sys
import pathlib
# sys.path.insert(1, pathlib.Path.cwd().parent.__str__())
# from backend.generation_utils.update_checker import UpdateChecker
from backend.generation_utils.update_checker import UpdateChecker

# from .generation_utils.update_checker import UpdateChecker
# import backend.generation_utils.update_checker

app = Flask(__name__)
app.debug = True
CORS(app)

# configure logging
# this file uses the custom logging class, because it is currently only working with this class
# TODO use custom logging class for the other logging parts of the system as well
# wirom_logger = Wirom_logger("app.log")

# routing_key lookup
with open(pathlib.Path.cwd() / 'backend' / 'routing_keys_lookup.json') as reader_file:
    # with open(pathlib.Path.cwd() / 'backend ' / 'routing_keys_lookup.json') as reader_file:
    routing_key_lookup = json.load(reader_file)
    # print(f"Routing lookup table:\n{routing_key_lookup}")

with open(pathlib.Path.cwd() / 'backend' / 'config.json') as json_data_file:
    data = json.load(json_data_file)
    robots = data["robots"]


@app.route('/mission', methods=['POST'])
def receive_mission():
    # wirom_logger.info("receive_mission")
    mission = request.get_json()

    # if not mission:
    #     print(f"No missions received")
    #     return 'No missions received', 200

    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.exchange_declare(exchange='routing_exchange', exchange_type='direct')


    for robot in mission:
        sequence = []
        for simpleaction in mission[robot]['simpleactions']:
            if simpleaction['args'] == "":
                sequence.append(simpleaction['name'] + "()")
            else:
                if simpleaction['name'] == 'set_message_target':
                    sequence.append(
                        simpleaction['name'] + "(" + "'" + simpleaction['args'] + "'" + ")")
                else:
                    sequence.append(
                        simpleaction['name'] + "(" + simpleaction['args'] + ")")

        success = False
        retries = 0

        # while not success or retries <= 60:
        #     try:
        #         port = mission[robot]["port"]
        #         current_routing_key = routing_key_lookup[port]
        #         channel.basic_publish(exchange="routing_exchange", routing_key=current_routing_key, body=)

        while not success and retries <= 60:
            try:
                # TODO this should normally be uncommented
                # requests.post('http://localhost:' + mission[robot]['port'] + '/simpleactions', json=sequence)
                # TODO this will send one sequence per task defined in "Tasks" in a mission
                # test_sending_one_message(sequence)

                # test_send_routing_messages(json.dumps(sequence), "moose_queue")
                # print("Sending sequence to " + mission[robot]['port'])
                port = mission[robot]['port']
                # print(f"port: {port}, type: {type(port)}")
                current_routing_key = routing_key_lookup[mission[robot]['port']]
                print(f"Sending sequence to robot {mission[robot]['port']}, queue_name={current_routing_key}")
                # print(f'Sequence:\n{sequence}\nType: {type(sequence)}')
                # test_send_routing_messages(json.dumps(sequence), routing_key)
                channel.basic_publish(
                    exchange="routing_exchange", routing_key=current_routing_key, body=json.dumps(sequence)
                )
                success = True
            except Exception as e:
                print(f"Exception: {e}")
                retries += 1
                print('Retry: ' + str(retries) + '...')
                time.sleep(1)
    connection.close()

    return 'Controllers successfully created', 200


@app.route('/allocate', methods=['POST'])
def receive_tasks_for_allocation():
    # wirom_logger.info("receive_tasks_for_allocation")
    tasks = request.get_json()
    tasks = task_allocation(tasks, robots)
    return jsonify(tasks)


# automatic task allocation algorithm, auction-based solution
# allocates tasks to robots based on highest bid
def task_allocation(tasks, robots):
    # wirom_logger.info("task_allocation")
    bids = {}
    for task in tasks:
        bids[task["name"]] = {}
        for robot in robots:
            bids[task["name"]][robot] = {}
            bid = 1
            for simpleaction in task["simpleactions"]:
                robot_simpleaction = list(filter(
                    lambda robot_simpleaction: robot_simpleaction["name"] == simpleaction["name"],
                    robots[robot]["simpleactions"]))
                if robot_simpleaction != []:
                    robot_simpleaction[0].update({"args": simpleaction["args"]})
                    robot_simpleaction[0].update({"location": robots[robot]["location"]})

                    utility = calculate_utility(robot_simpleaction[0])
                    bid = bid * utility
                else:
                    bid = 0
            bids[task["name"]][robot] = bid

    tasks = allocate_tasks_to_highest_bidder(tasks, bids)
    return tasks


# Calculate the utility a robot has for a simpleaction (quality - cost)
def calculate_utility(robot_simpleaction):
    utility = robot_simpleaction["quality"] - robot_simpleaction["cost"]
    # calculate cross dependencies: go to location only such simpleaction for now
    if robot_simpleaction["name"] == "go_to_location" and robot_simpleaction["args"] != "[]":
        robot_loc = robot_simpleaction["location"]
        targetlist = robot_simpleaction["args"].strip('][').split(', ')
        target = {"x": int(targetlist[0]), "y": int(targetlist[1])}
        distance = abs(robot_loc["x"] - target["x"] +
                       robot_loc["y"] - target["y"])
        # find distance from target location and normalize before adding to utility
        distNorm = (1 - distance / 100)
        if distNorm > 0.1:
            utility = utility * distNorm
        else:
            utility = utility * 0.1

    return utility


# Sorting bids and allocates tasks to robots based on highest bid
def allocate_tasks_to_highest_bidder(tasks, bids):
    for bid in bids:
        highest_bidder = '--'
        for robot in bids[bid]:
            if highest_bidder == '--' and bids[bid][robot] > 0:
                highest_bidder = robot
            elif highest_bidder != '--' and bids[bid][robot] > bids[bid][highest_bidder]:
                highest_bidder = robot

        for task in tasks:
            if task["name"] == bid:
                task["robot"] = highest_bidder

    return tasks


@app.route('/ping')
def ping():
    return 'Pong!'


# def test_communication_messages(msg):
#     # Test. Send 10 messages, with a time interval of 3 seconds between each message

#     # inititate message communication
#     connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
#     channel = connection.channel()

#     channel.exchange_declare(exchange='test_exchange', exchange_type='fanout')

#     count = 0
#     while count < 10:
#         msg = "Test message number " + str(count)
#         # message = "This is a test message"
#         channel.basic_publish(exchange='test_exchange', routing_key='', body=msg)
#         wirom_logger.info("(app) sent message %r" % msg)
#         print("(app) sent message %r" % msg)

#         time.sleep(3)
#         count += 1
#     connection.close()


def test_sending_one_message(sequence):
    # Test. Send 10 messages, with a time interval of 3 seconds between each message

    # inititate message communication
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.exchange_declare(exchange='test_exchange', exchange_type='fanout')
    print(f'sequence: {sequence}')
    msg = "go_backward(2),turn_left(3)"
    channel.basic_publish(exchange='test_exchange', routing_key='', body=msg)
    connection.close()


def test_send_routing_messages(message_as_json, routing_key):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.exchange_declare(exchange='routing_exchange', exchange_type='direct')
    channel.basic_publish(exchange='routing_exchange', routing_key=routing_key, body=message_as_json)
    print(f"[send_routing_message] published to {routing_key}")

    connection.close()


if __name__ == '__main__':
    # wirom_logger.info("initiated main")
    print("initiated main")
    # app.run(processes='5', debug=True)
    # app.run(threaded=True)

    # test_message = "Hello this message is from __init__.py"
    # test_communication_messages(test_message)

# When starting the server, check if there has been any updates of robots
update_checker = UpdateChecker()
update_checker.initiate_full_robot_check()
