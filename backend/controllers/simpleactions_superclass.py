from controller import Robot
import pika
import json


class SimpleactionsSuperclass:
    def __init__(self, name):
        # create the Robot instance.
        self.robot = Robot()
        self.robot_name = name

        # get the time step of the current world.
        self.timestep = int(self.robot.getBasicTimeStep())

        # self.available_simpleactions = {}
        self.simpleactions = []
        print(f"Super class initiated. {self.robot_name}")

    # def add_available_simpleaction(self, name, function_reference):
    #     self.available_simpleactions[name] = function_reference
    #


    def receive_routing_message(self):
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        channel = connection.channel()
        channel.exchange_declare(exchange='routing_exchange', exchange_type='direct')

        result = channel.queue_declare(queue='', exclusive=True)
        queue_name = result.method.queue

        channel.queue_bind(exchange='routing_exchange', queue=queue_name, routing_key=f"{self.robot_name}_queue")

        print(f"{self.robot_name} ready to receive routed messages")
        channel.basic_consume(queue=queue_name, on_message_callback=self.execute_simpleactions_callback, auto_ack=True)

        channel.start_consuming()


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
            print(f"{self.robot_name} Executing simpleaction " + sim_act)
            eval("self." + sim_act)
        print(f"{self.robot_name} finished callback function")