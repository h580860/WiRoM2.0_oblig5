"""moose_controller simpleactions."""
from controller import Robot, Motor, PositionSensor, GPS, Compass
# from flask import Flask, request
import math
import threading
import time
import json
import logging
import os
import pika
from simpleactions_superclass import SimpleactionsSuperclass
from message_subscriber import MessageSubscriber


class MooseSimpleactionsGenerator(SimpleactionsSuperclass):
    def __init__(self, name):
        super().__init__(name, "moose")
        # create the Robot instance.
        # self.robot = Robot()
        # self.robot_name = name

        # get the time step of the current world.
        self.timestep = int(self.robot.getBasicTimeStep())

        self.left_motor_names = ["left motor 1", "left motor 2",
                                 "left motor 3", "left motor 4"]
        self.right_motor_names = ["right motor 1",
                                  "right motor 2", "right motor 3", "right motor 4"]
        self.left_motors = [self.robot.getDevice(name) for name in self.left_motor_names]
        self.right_motors = [self.robot.getDevice(name) for name in self.right_motor_names]
        self.left_speed = 0
        self.right_speed = 0

        # get and enable nodes used by the robot
        self.gps = self.robot.getDevice('gps')
        self.compass = self.robot.getDevice('compass')
        self.gps.enable(self.timestep)
        self.compass.enable(self.timestep)

        self.target_reached = False
        self.navigate = False
        self.location = []
        # simpleactions = ["go_forward(3)", "turn_right(2)", "go_forward(2)"]
        # self.simpleactions = []

        # self.initiate_threads()
        self.add_all_simpleactions()

        # The moose needs to listen to a queue for receiving locations
        self.location_binding_key = f"{self.robot_name}_location_queue"
        self.location_exchange = "location_exchange"
        self.location_exchange_type = "direct"
        self.locations_subscriber = MessageSubscriber(
            self.location_binding_key, self.location_exchange, self.location_exchange_type, self.receive_location_callback)

    def add_all_simpleactions(self):
        self.add_available_simpleaction("go_forward", self.go_forward)
        self.add_available_simpleaction("go_backward", self.go_backward)
        self.add_available_simpleaction("turn_right", self.turn_right)
        self.add_available_simpleaction("turn_left", self.turn_left)
        self.add_available_simpleaction("go_to_location", self.go_to_location)
        self.add_available_simpleaction("stop_movement", self.stop_movement)
        self.add_available_simpleaction("receive_location_from_robot", self.receive_location_from_robot)

    def initiate_threads(self):
        main = threading.Thread(target=self.moose_main)
        # communication = threading.Thread(target=self.receive_routing_message)
        # location_communication = threading.Thread(target=self.receive_location)
        communication = threading.Thread(target=self.simpleactions_subscriber.subscription)
        location_communication = threading.Thread(target=self.locations_subscriber.subscription)

        main.start()
        communication.start()
        # communication.start()
        location_communication.start()

    def go_forward(self, duration):
        self.left_speed = 7.0
        self.right_speed = 7.0
        if duration != 0:
            print(f"Moose sleeping for {duration} seconds")
            time.sleep(duration)
            self.left_speed = 0
            self.right_speed = 0

    def go_backward(self, duration):
        self.left_speed = -2.0
        self.right_speed = -2.0
        if duration != 0:
            time.sleep(duration)
            self.left_speed = 0
            self.right_speed = 0

    def turn_left(self, duration):
        self.left_speed = 1.0
        self.right_speed = 4.0
        if duration != 0:
            time.sleep(duration)
            self.left_speed = 0
            self.right_speed = 0

    def turn_right(self, duration):
        self.left_speed = 4.0
        self.right_speed = 1.0
        if duration != 0:
            time.sleep(duration)
            self.left_speed = 0
            self.right_speed = 0

    def go_to_location(self, target):
        if not self.location and target:
            self.location = [target]

        self.navigate = True
        while self.navigate:
            time.sleep(1)

    def stop_movement(self):
        self.left_speed = 0
        self.right_speed = 0

    # Function that finds the angle and distance to a location and moves the vehicle accordingly
    def navigate_to_location(self):
        loc = self.location[0]

        pos = self.gps.getValues()
        north = self.compass.getValues()
        front = [-north[0], north[1], north[2]]

        dir = [loc[0] - pos[0], loc[1] - pos[2]]
        distance = math.sqrt(dir[0] * dir[0] + dir[1] * dir[1])

        # calculate the angle of which the vehicle is supposed to go to reach target
        angle = math.atan2(dir[1], dir[0]) - math.atan2(front[2], front[0])
        if angle < 0:
            angle += 2 * math.pi

        # vehicle is on the right path when angle = math.pi
        if angle < math.pi - 0.01:
            self.turn_left(0)
        elif angle > math.pi + 0.01:
            self.turn_right(0)
        else:
            self.go_forward(0)

        # stop vehicle and navigation when target has been reached
        if distance < 1:
            print('Reached target')
            self.navigate = False
            self.location.pop(0)
            self.stop_movement()

    # Actively wait for new location
    def receive_location_from_robot(self, ):
        while not self.location:
            time.sleep(1)

    # write the location of this robot to the config file
    def setLocationConfig(self):
        with open('../../config.json') as json_data_file:
            data = json.load(json_data_file)

        with open('../../config.json', 'w') as json_data_file:
            data['robots']['moose']['location'] = {
                "x": self.gps.getValues()[0], "y": self.gps.getValues()[2]}
            json.dump(data, json_data_file, indent=2, sort_keys=True)

    def moose_main(self):
        step_count = 0
        for motor in self.left_motors:
            motor.setPosition(float('inf'))
        for motor in self.right_motors:
            motor.setPosition(float('inf'))

        while self.robot.step(self.timestep) != -1:
            if self.navigate:
                self.navigate_to_location()
            for motor in self.left_motors:
                motor.setVelocity(self.left_speed)
            for motor in self.right_motors:
                motor.setVelocity(self.right_speed)
            # print(f'(moose) step number {step_count}')
            step_count += 1
            # logging.info(step_count)
            # print("main iteration")

    def receive_topic_message_callback(self, ch, method, properties, body):
        print(f"{self.robot_name} receive_topic_message_callbacks")
        print(f"method.routin_key: {method.routing_key}")
        if "location" in method.routing_key:
            self.receive_location_callback(ch, method, properties, body)
        else:
            self.execute_simpleactions_callback(ch, method, properties, body)

    # def receive_location(self):
    #     connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    #     channel = connection.channel()
    #     channel.exchange_declare(exchange='location_exchange', exchange_type='direct')
    #
    #     result = channel.queue_declare(queue='', exclusive=True)
    #     queue_name = result.method.queue
    #
    #     channel.queue_bind(exchange='location_exchange', queue=queue_name,
    #                        routing_key=f"{self.robot_name}_location_queue")
    #
    #     print(f"{self.robot_name} ready to receive locations")
    #     channel.basic_consume(queue=queue_name, on_message_callback=self.receive_location_callback, auto_ack=True)
    #     channel.start_consuming()
    #
    def receive_location_callback(self, ch, method, properties, body):
        print(f"{self.robot_name} received locations")

        new_location = json.loads(body.decode('utf-8'))
        # print(f"new location={new_location}, type = {type(new_location)}")
        self.location.append(new_location['location'])
