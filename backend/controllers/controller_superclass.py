from controller import Robot
import pika
import json
import string
import ast
import threading
import pathlib
import time
import os
import sys
from message_subscriber import MessageSubscriber

# This is a "workaround" to be able to import the class when the controllers are running in the
# Webots "sandbox". So we need to add the current working directory as well as "two parents steps up".
cbaa_path = os.path.join(os.getcwd(), os.pardir)
cbaa_path = os.path.join(cbaa_path, os.pardir)
sys.path.insert(0, cbaa_path)
from task_allocation.cbaa import CBAA


class ControllerSuperclass:
    def __init__(self, name, robot_type):
        '''
        Super class for the simpleactions generators, with the most common functionalities. Each robot type
        class extends this class
        '''
        # create the Robot instance.
        self.robot = Robot()
        self.robot_name = name
        self.robot_type = robot_type
        # get the time step of the current world.
        self.timestep = int(self.robot.getBasicTimeStep())

        self.available_simpleactions_functions = {}
        self.simpleactions = []

        # List of simpleaction from the configuration file
        self.config_simpleactions_names_cost = {}

        # Initiate the topics subscriber
        self.binding_key = f"{name}_queue"
        self.exchange = "routing_exchange"
        self.exchange_type = "direct"
        self.simpleactions_subscriber = MessageSubscriber(
            self.binding_key, self.exchange, self.exchange_type, self.execute_simpleactions_callback
        )

        # Create subscriber for listening to the CBAA task allocation updates
        # we can give it an empty binding key, because the 'fanout' exchange will ignore its value
        # either way
        cbaa_exchange_name = "cbaa_initiate_exchange"
        cbaa_exchange_type = "fanout"
        self.cbaa_subscriber = MessageSubscriber(
            "", cbaa_exchange_name, cbaa_exchange_type, self.initiate_cbaa_callback
        )

        # Initiate thread for listening to the CBAA task allocation initiation from the server
        cbaa_initiation_communication = threading.Thread(target=self.cbaa_subscriber.subscription)
        cbaa_initiation_communication.start()

        # Create a Subscription for receiving bids from the other robots
        self.cbaa_bids_exchange_name = "cbaa_bids_exchange"
        self.cbaa_bids_subscriber = MessageSubscriber(
            "", self.cbaa_bids_exchange_name, cbaa_exchange_type, self.receive_cbaa_bids_callback
        )
        # Initiate a thread for receiving the bids from the other robots
        cbaa_bids_communication = threading.Thread(target=self.cbaa_bids_subscriber.subscription)
        cbaa_bids_communication.start()

        # Read the config data to get the available simpleactions for this robot type
        self.read_config_data()


        # TODO this should somehow be dynamic
        # self.n_robots = 4
        self.consensus_based_auction_algorithm = CBAA(
            # self.robot_name, self.test_avail_simpleactions, self.n_robots
            self.robot_name, self.config_simpleactions_names_cost, self.n_robots
        )

        print(f"Super class initiated. {self.robot_name}")

    def read_config_data(self):
        """
        Reads the configuration file
        """
        with open(pathlib.Path.cwd().parent.parent / 'config.json') as json_config_file:
            data = json.load(json_config_file)
            self.n_robots = len(data["robots"])
            for x in data["robots"][self.robot_type]["simpleactions"]:
                self.config_simpleactions_names_cost[x["name"]] = float(x["cost"])

    def add_available_simpleaction(self, name, function_reference):
        self.available_simpleactions_functions[name] = function_reference

    def execute_simpleactions_callback(self, ch, method, properties, body):
        print(f"{self.robot_name} callback: %r" % body)
        # TODO as for now, the incoming messages are functions calls, separated by ","
        # simpleactions.extend(body.decode('utf-8').split(","))

        # Decode the JSON back to a list
        new_simpleactions = json.loads(body.decode('utf-8'))
        self.simpleactions.extend(new_simpleactions)
        print(f'{self.robot_name} Simpleactions = {self.simpleactions}, type={type(self.simpleactions)}')

        # Now execute the simpleactions
        # for i in range(len(simpleactions)):
        while self.simpleactions:
            sim_act = self.simpleactions.pop(0)
            print(f"sim_act = {sim_act}")
            print(f"Function name = {sim_act['function_name']}, Args = {sim_act['args']}")
            function_name = sim_act['function_name']
            args = sim_act['args']
            # Retrieve the args
            # function_name = sim_act.split('(')[0]
            # args = sim_act.split('(')[1].split(')')[0]
            #
            if not args:
                self.available_simpleactions_functions[function_name]()
                continue
            # Convert the arguments
            if all([x in string.digits for x in args]):
                print(f"{args} is a number")
                args = int(args)
            elif "[" in args or "]" in args:
                # ast.literal_eval will safely evaluate the string representation of a list (with the square brackets
                # as well) to a python list
                args = ast.literal_eval(args)

            self.available_simpleactions_functions[function_name](args)

        print(f"{self.robot_name} finished callback function")

    def receive_cbaa_bids_callback(self, ch, method, properties, body):
        all_bids = json.loads(body)
        print(f"{self.robot_name} received: {all_bids}")
        for other_robot_name, bids in all_bids.items():
            if self.robot_name == other_robot_name:
                # Skip the bid of this robot
                continue
            self.consensus_based_auction_algorithm.receive_other_winning_bids(other_robot_name, bids)

    def publish_bids(self, bids):
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))
        channel = connection.channel()

        channel.exchange_declare(exchange=self.cbaa_bids_exchange_name, exchange_type='fanout')

        # message = f"Bids by {self.robot_name}: {bids}"
        message = {self.robot_name : bids}
        channel.basic_publish(exchange=self.cbaa_bids_exchange_name, routing_key='', body=json.dumps(message))
        # print(" [x] Sent %r" % message)
        connection.close()

    def initiate_cbaa_callback(self, ch, method, properties, body):
        print(f'{self.robot_name} initiate cbaa callback function, received {body}')
        # time.sleep(1)
        # self.publish_bids()
        new_available_tasks = json.loads(body.decode('utf-8'))
        # print(f"new_available_tasks = {new_available_tasks}")
        # new_task_lists = []
        # for task in new_available_tasks:
        #     new_task_lists.append(task["simpleactions"])
        # print(f"new_task_list = {new_task_lists}")
        self.consensus_based_auction_algorithm.add_task_list(new_available_tasks)
        # self.consensus_based_auction_algorithm.add_task_list(new_task_lists)

        # Phase 1
        self.consensus_based_auction_algorithm.select_task()

        # Phase 2
        # self.consensus_based_auction_algorithm.update_task()
        bids = self.consensus_based_auction_algorithm.get_winning_bids()
        self.publish_bids(bids)

        self.consensus_based_auction_algorithm.confirm_all_bids(self.robot_name)

        self.consensus_based_auction_algorithm.update_task()

        # Finally, publish the results
        # winning_robots = self.consensus_based_auction_algorithm.winning_robots
        # self.send_cbaa_result_to_server(winning_robots)
        self.consensus_based_auction_algorithm.post_results()
        # After posting the consensus to the server, reset the values in the CBAA Class
        self.consensus_based_auction_algorithm.cleanup()


    # def send_cbaa_result_to_server(self, winning_robots):
    #     """
    #     Publish the winning robots to the server, using the 'routing_exchange' exchange which is commonly used
    #     to publish the simpleactions to the server
    #     """
    #     connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    #     channel = connection.channel()
    #
    #     exchange_name = 'routing_exchange'
    #     routing_key = 'server_queue'
    #     message = json.dumps(winning_robots)
    #
    #     channel.exchange_declare(exchange=exchange_name, exchange_type='direct')
    #     channel.basic_publish(exchange=exchange_name, routing_key=routing_key, body=message)
    #     print(f"{self.robot_name} published it winning bid list")
    #     connection.close()
