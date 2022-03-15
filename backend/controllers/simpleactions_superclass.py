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


class SimpleactionsSuperclass:
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

        self.available_simpleactions = {}
        self.simpleactions = []

        # List of simpleaction from the configuration file
        self.config_simpleactions = []

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

        # Read the config data
        self.read_config_data()

        print(f"Super class initiated. {self.robot_name}")

    def read_config_data(self):
        """
        Reads the configuration file
        """
        with open(pathlib.Path.cwd().parent.parent / 'config.json') as json_config_file:
            data = json.load(json_config_file)
            self.config_simpleactions = data["robots"][self.robot_type]["simpleactions"]

    def add_available_simpleaction(self, name, function_reference):
        self.available_simpleactions[name] = function_reference

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
                self.available_simpleactions[function_name]()
                continue
            # Convert the arguments
            if all([x in string.digits for x in args]):
                print(f"{args} is a number")
                args = int(args)
            elif "[" in args or "]" in args:
                # ast.literal_eval will safely evaluate the string representation of a list (with the square brackets
                # as well) to a python list
                args = ast.literal_eval(args)

            self.available_simpleactions[function_name](args)

        print(f"{self.robot_name} finished callback function")

    def receive_cbaa_bids_callback(self, ch, method, properties, body):
        print(f"{self.robot_name} receive {body}")

    def publish_bids(self):
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))
        channel = connection.channel()

        channel.exchange_declare(exchange=self.cbaa_bids_exchange_name, exchange_type='fanout')

        message = f"Bids by {self.robot_name}"
        channel.basic_publish(exchange=self.cbaa_bids_exchange_name, routing_key='', body=message)
        # print(" [x] Sent %r" % message)
        connection.close()

    def initiate_cbaa_callback(self, ch, method, properties, body):
        # print(f'{self.robot_name} initiate cbaa callback function, received {body}')
        every_simpleaction_name = [x["name"] for x in self.config_simpleactions]
        print(f"{self.robot_name} of type {self.robot_type} has these available simpleactions:"
              f"{every_simpleaction_name}")
        # time.sleep(1)
        # self.publish_bids()
        
