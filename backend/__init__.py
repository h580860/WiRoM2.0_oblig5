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
import pprint
import importlib

# sys.path.insert(1, pathlib.Path.cwd().parent.__str__())
# from backend.generation_utils.update_checker import UpdateChecker
from backend.generation_utils.update_checker import UpdateChecker
from backend.controllers.message_subscriber import MessageSubscriber
from backend.generation_utils.dsl_shellcommands import DSLShellCommands
from backend.new_task_allocation_algorithms import *
# from backend.new_task_allocation_algorithms.random_allocation import random_allocation
from backend.new_task_allocation_algorithms.random_allocation import RandomAllocation
from backend.task_allocation.original_task_allocation import OriginalTaskAllocation

# from .generation_utils.update_checker import UpdateChecker
# import backend.generation_utils.update_checker

app = Flask(__name__)
app.debug = True
CORS(app)

# A dictionary to keep track of the added algorithm names
# The keys are the algorithm names, and the values are the corresponding function call
# UPDATED: The keys are the algorithm names, and the values are the corresponding classes
added_algorithms = {"random_allocation": RandomAllocation(
    "random_allocation").random_allocation}


# The location of the script used to run the DSL code generation
script_location_filepath = pathlib.Path().parent / "robot-generator"
# Utility class for executing the DSL Langium commands in a Python class
dsl_shell_commands = DSLShellCommands(script_location_filepath)

# Printer to "pretty print" JSON/dictionary objects
pp = pprint.PrettyPrinter()

"""
TODO a big note here is that flask is neither thread safe or process safe so we can normally get race conditions if
multiple requests are trying to access the same data. However, this will not be the case here, as the user is only
allowed to call this request once before waiting for it to finish
https://stackoverflow.com/questions/32815451/are-global-variables-thread-safe-in-flask-how-do-i-share-data-between-requests
"""
cbaa_results = []

# Initiate task allocation classes
original_task_allocation = OriginalTaskAllocation("task_allocation")

# routing_key lookup
# with open(pathlib.Path.cwd() / 'backend' / 'routing_keys_lookup.json') as reader_file:
# with open(pathlib.Path.cwd() / 'backend ' / 'routing_keys_lookup.json') as reader_file:
# routing_key_lookup = json.load(reader_file)
# print(f"Routing lookup table:\n{routing_key_lookup}")

with open(pathlib.Path.cwd() / 'backend' / 'config.json') as json_data_file:
    data = json.load(json_data_file)
    robots = data["robots"]


@app.route('/cbaa_initiation', methods=['POST'])
def initiate_cbaa():
    # wirom_logger.info("receive_tasks_for_allocation")
    tasks = request.get_json()
    print(f"Server received tasks: {tasks}")
    print()
    pp.pprint(tasks)
    # TODO FINISHED HERE 16.03.2022 16.27

    # The tasks currently needs to be formatted before they are published to the robots
    formatted_task_list = []
    for t in tasks:
        formatted_task_list.append({
            "name": t["name"],
            # "simpleactions": t["simpleactions"]["name"]
            "simpleactions": [x["name"] for x in t["simpleactions"]]
        })
    print(f"formatted task list = {formatted_task_list}")
    send_task_list(json.dumps(formatted_task_list))

    while not cbaa_results:
        time.sleep(1)
    print(
        f"cbaa_initiation finished. Global cbaa_results variable = {cbaa_results}")

    # TODO check that all of the bids consensus are the same over the different robots

    consensus = cbaa_results[0]
    print("consensus")
    pp.pprint(consensus)
    print(consensus)

    # Reformat the results to be sent back to the frontend
    new_allocation = []
    for i in range(len(tasks)):
        new_consensus = consensus[i]
        for original_task in tasks:
            if original_task["name"] == new_consensus["name"]:
                original_task["robot"] = new_consensus["robot"]
                # new_allocation.append(original_task)
                break

    print("New Allocation:")
    pp.pprint(tasks)

    return jsonify(tasks)


def send_task_list(task_list_as_json):
    print("Sending the task list to the robots")
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.exchange_declare(
        exchange='cbaa_initiate_exchange', exchange_type='fanout')

    channel.basic_publish(exchange='cbaa_initiate_exchange',
                          routing_key='', body=task_list_as_json)
    connection.close()


@app.route('/cbaa_results', methods=['POST'])
def receive_cbaa_results():
    result = request.get_json()
    cbaa_results.append(result)
    print(f"Received results: {result}")
    return 'Server received winning bids', 200


@app.route('/mission', methods=['POST'])
def receive_mission():
    # wirom_logger.info("receive_mission")
    mission = request.get_json()

    # if not mission:
    #     print(f"No missions received")
    #     return 'No missions received', 200

    # connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    # channel = connection.channel()
    # channel.exchange_declare(exchange='routing_exchange', exchange_type='direct')

    # for robotname, value in mission.items():
    for robot in mission:
        sequence = []
        for simpleaction in mission[robot]['simpleactions']:
            sequence.append(
                {'function_name': simpleaction['name'], 'args': simpleaction['args']})

            # if simpleaction['args'] == "":
            #     sequence.append(simpleaction['name'] + "()")
            # else:
            #     if simpleaction['name'] == 'set_message_target':
            #         sequence.append(
            #             simpleaction['name'] + "(" + "'" + simpleaction['args'] + "'" + ")")
            #     else:
            #         sequence.append(
            #             simpleaction['name'] + "(" + simpleaction['args'] + ")")

        success = False
        retries = 0

        # while not success or retries <= 60:
        #     try:
        #         port = mission[robot]["port"]
        #         current_routing_key = routing_key_lookup[port]
        #         channel.basic_publish(exchange="routing_exchange", routing_key=current_routing_key, body=)

        while not success and retries <= 60:
            try:
                # TODO this will send one sequence per task defined in "Tasks" in a mission
                # test_sending_one_message(sequence)

                # test_send_routing_messages(json.dumps(sequence), "moose_queue")
                # print("Sending sequence to " + mission[robot]['port'])
                port = mission[robot]['port']
                # print(f"port: {port}, type: {type(port)}")
                # current_routing_key = routing_key_lookup[mission[robot]['port']]
                # print(f"Sending sequence to robot {mission[robot]['port']}, queue_name={current_routing_key}")
                current_routing_key = f"{robot}_queue"
                # print(f'Sequence:\n{sequence}\nType: {type(sequence)}')
                test_send_routing_messages(
                    json.dumps(sequence), current_routing_key)
                # channel.basic_publish(
                # exchange="routing_exchange", routing_key=current_routing_key, body=json.dumps(sequence))
                success = True
            except Exception as e:
                print(f"Exception: {e}")
                retries += 1
                print('Retry: ' + str(retries) + '...')
                time.sleep(1)
    # connection.close()

    return 'Controllers successfully created', 200


@app.route('/allocate', methods=['POST'])
def receive_tasks_for_allocation():
    # wirom_logger.info("receive_tasks_for_allocation")
    tasks = request.get_json()
    # print(f"tasks:\n{tasks}")
    # for t in tasks:
    #     print(t)
    print("Tasks received:")
    pp.pprint(tasks)
    # tasks = task_allocation(tasks, robots)
    tasks = original_task_allocation.task_allocation(tasks, robots)
    return jsonify(tasks)


@app.route('/robot-generator', methods=['POST'])
def generate_dsl_code():
    editor_content = request.get_json()
    commands = editor_content["content"].split("\n")
    print(f"Received: {editor_content}.\nCommand list = {commands}")

    if len(commands) == 1 and commands[0] == '':
        print(f"No commands!")
        return jsonify({"success": True, "output": ["No content sent"]}), 400

    # Write the received commands to the proper .robotgenerator file
    # TODO hard coded file location
    file_location = pathlib.Path().parent / "robot-generator" / \
        "example" / "testDsl.robotgenerator"
    with open(file_location, "w") as f:
        for x in commands:
            f.write(x + "\n")

    # Run the commands for generating the DSL in Langium, through the static methods in the Python helper class

    generation_results = dsl_shell_commands.generate_dsl_code_command()
    print(f"generation_result = {generation_results}")

    # Extract the output, split it up on newlines and filter out the empty elements
    output = list(filter(lambda x: x != "",
                  generation_results.stdout.split("\n")))

    error_output = list(filter(lambda x: x != "",
                               generation_results.stderr.split("\n")))

    if generation_results.returncode == 1:
        return jsonify({"success": False, "output": error_output}), 400

    else:
        update_checker = UpdateChecker()
        update_checker.update_everything_after_dsl_usage()
        return jsonify({"success": True, "output": output}), 200


@app.route('/deleteGeneratedDSL', methods=['POST'])
def delete_dsl_code():
    print("Server received request to delete the generated DSL files")
    deletion_results = dsl_shell_commands.delete_generated_files_command()

    # Extract the output, split it up on newlines and filter out the empty elements
    output = list(filter(lambda x: x != "",
                  deletion_results.stdout.split("\n")))

    error_output = list(filter(lambda x: x != "",
                               deletion_results.stderr.split("\n")))
    print(f"Error output = {error_output}")
    if deletion_results.returncode == 1:
        return jsonify({"success": False, "output": error_output}), 400

    else:
        return jsonify({"success": True, "output": output}), 200

    return "Success", 200


@app.route('/ping')
def ping():
    return 'Pong!'


@app.route('/new-algorithm', methods=['POST'])
def add_new_algorithm():
    name = request.get_json()["algorithm_name"]
    editor_content = request.get_json()["content"]
    print(f"Algorithm name: {name}")
    print(f"Editor content:\n{editor_content}")

    code_lines = editor_content.split("\n")
    new_filepath = pathlib.Path().parent / "backend" / \
        "new_task_allocation_algorithms" / f"{name}.py"
    print(f"newfilepath = {new_filepath}")

    with open(new_filepath, 'w') as writer:
        # First we need to manually write some lines

        # It is useful to import the random library just in case the user wants to
        # utilize it
        writer.write("import random\n")
        # Need to import the parent class
        writer.write(
            "from ..task_allocation.centralized_taskallocation import CentralicedTaskAllocation\n")

        # write the class name, including its parent class
        writer.write(f"class {name}(CentralicedTaskAllocation):\n")
        writer.write(f"\tdef __init__(self, algorithm_name):\n")
        writer.write(f"\t\tsuper().__init__(algorithm_name)\n\n")
        for l in code_lines:
            writer.write("\t" + l + "\n")

    # TEST call function
    # source: https://stackoverflow.com/questions/3061/calling-a-function-of-a-module-by-using-its-name-a-string

    # test_filename = "backend/new_task_allocation_algorithms/test"
    # function_name = "func"
    # module = __import__(test_filename)
    # func = getattr(module, function_name)
    # func()

    # Source: https://stackoverflow.com/questions/301134/how-to-import-a-module-given-its-name-as-string
    # Also source directly from the question at:
    # https://stackoverflow.com/questions/44492803/python-dynamic-import-how-to-import-from-module-name-from-variable/44492879#44492879
    # my_module = importlib.import_module(
    #     "backend.new_task_allocation_algorithms.test")
    # my_module.func()

    test_module = importlib.import_module(
        f"backend.new_task_allocation_algorithms.{name}")
    new_class = getattr(test_module, name)
    # print(f"New class: {new_class}")
    new_algorithm_instance = new_class(name)
    method_to_call = getattr(new_algorithm_instance, name)
    # method_to_call = getattr(new_algorithm_instance, "display_name")
    # print(f"method to call: {method_to_call}")
    # getattr(new_algorithm_instance, "display_name")()
    # added_algorithms[name] = method_to_call(name)
    added_algorithms[name] = method_to_call
    # method_to_call()
    # print(f"added_algorithms dictionary: {added_algorithms}")

    return jsonify({"success": True, "name": name}), 200


@app.route('/execute-algorithm', methods=['POST'])
def execute_new_task_allocation_algorithm():
    name = request.get_json()["name"]
    tasks = request.get_json()["tasks"]
    print(f"Server received function name: {name}")
    print(f"Server received tasks:")
    pp.pprint(tasks)

    print("Robots:")
    pp.pprint(robots)

    allocated_tasks = added_algorithms[name](tasks, robots)

    # return jsonify({"success": True, "message": f"Successfully executed the fucntion {name}"}), 200
    return jsonify(allocated_tasks)


def test_sending_one_message(sequence):
    # Test. Send 10 messages, with a time interval of 3 seconds between each message

    # inititate message communication
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.exchange_declare(exchange='test_exchange',
                             exchange_type='fanout')
    print(f'sequence: {sequence}')
    msg = "go_backward(2),turn_left(3)"
    channel.basic_publish(exchange='test_exchange',
                          routing_key='', body=msg)
    connection.close()


def test_send_routing_messages(message_as_json, routing_key):
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.exchange_declare(
        exchange='routing_exchange', exchange_type='direct')
    channel.basic_publish(exchange='routing_exchange',
                          routing_key=routing_key, body=message_as_json)
    print(f"[send_routing_message] published to {routing_key}")

    connection.close()


if __name__ == '__main__':
    # wirom_logger.info("initiated main")
    print("initiated main")
    # app.run(processes='5', debug=True)
    # app.run(threaded=True)

    # test_message = "Hello this message is from __init__.py"
    # test_communication_messages(test_message)
