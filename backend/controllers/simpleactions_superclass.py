from controller import Robot
import pika
import json
import string
import ast
from message_subscriber import MessageSubscriber


class SimpleactionsSuperclass:
    def __init__(self, name):
        '''
        Super class for the simpleactions generators, with the most common functionalities
        '''
        # create the Robot instance.
        self.robot = Robot()
        self.robot_name = name
        # get the time step of the current world.
        self.timestep = int(self.robot.getBasicTimeStep())

        self.available_simpleactions = {}
        self.simpleactions = []

        # Initiate the topics subscriber
        self.binding_key = f"{name}_queue"
        self.exchange = "routing_exchange"
        self.simpleactions_subscriber = MessageSubscriber(
            self.binding_key, self.exchange,self.execute_simpleactions_callback
        )

        print(f"Super class initiated. {self.robot_name}")

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
