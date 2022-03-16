"""mavic2pro_controller simpleactions."""
from controller import Robot, Motor, PositionSensor, Gyro, Camera, InertialUnit, GPS, Compass, CameraRecognitionObject
# from flask import Flask, request
import requests
import math
import threading
import time
import json
import sys
import os
import logging
import pika
from simpleactions_superclass import SimpleactionsSuperclass


class Mavic2proSimpleactionsGenerator(SimpleactionsSuperclass):
    def __init__(self, name):
        test_avail_simpleactions = {"go_forward": 0.6, "turn_right": 0.8, "turn_left": 0.5, "go_backwards": 0.7}
        super().__init__(name, "mavic2pro", test_avail_simpleactions)

        # get the motors for the robot
        self.front_left_motor = self.robot.getDevice('front left propeller')
        self.front_right_motor = self.robot.getDevice('front right propeller')
        self.rear_left_motor = self.robot.getDevice('rear left propeller')
        self.rear_right_motor = self.robot.getDevice('rear right propeller')
        self.rear_right_motor = self.robot.getDevice('rear right propeller')
        self.motors = \
            [self.front_left_motor, self.front_right_motor, self.rear_left_motor, self.rear_right_motor]

        # get and enable nodes used by the robot
        self.gyro = self.robot.getDevice('gyro')
        self.iu = self.robot.getDevice('inertial unit')
        self.gps = self.robot.getDevice('gps')
        self.compass = self.robot.getDevice('compass')
        self.camera = self.robot.getDevice('camera')

        self.gyro.enable(self.timestep)
        self.iu.enable(self.timestep)
        self.gps.enable(self.timestep)
        self.compass.enable(self.timestep)
        self.camera.enable(self.timestep)

        # empirically found constants for the drone to perform stable flight; inspired by the drone demo controller
        self.k_vertical_thrust = 68.5  # with this thrust, the drone lifts.
        # Vertical offset where the robot actually targets to stabilize itself.
        self.k_vertical_offset = 0.6
        self.k_vertical_p = 3.0  # P constant of the vertical PID.
        self.k_roll_p = 50.0  # P constant of the roll PID.
        self.k_pitch_p = 30.0  # P constant of the pitch PID.

        # variables that control the movement of the drone
        self.target_altitude = 0
        self.roll_disturbance = 0
        self.pitch_disturbance = 0
        self.yaw_disturbance = 0

        # variables to set drone functions
        self.rec_obj_arr = []
        self.recognise = False
        self.navigate = False
        self.target_reached = False
        self.message_recipient = ''
        self.location = []
        self.target_loc = []
        self.simpleactions = []
        self.amount_of_objects = 0

        # self.initiate_threads()
        self.add_all_simpleactions()

    def add_all_simpleactions(self):
        self.add_available_simpleaction("set_altitude", self.set_altitude)
        self.add_available_simpleaction("go_forward", self.go_forward)
        self.add_available_simpleaction("go_backward", self.go_backward)
        self.add_available_simpleaction("turn_right", self.turn_right)
        self.add_available_simpleaction("turn_left", self.turn_left)
        self.add_available_simpleaction("recognise_objects", self.recognise_objects)
        self.add_available_simpleaction("go_to_location", self.go_to_location)
        self.add_available_simpleaction("set_message_target", self.set_message_target)
        self.add_available_simpleaction("send_location", self.send_location)
        self.add_available_simpleaction("stop_movement", self.stop_movement)


    # Initialize which sets the target altitude as well as start the main loop
    def initiate_threads(self):
        main = threading.Thread(target=self.mavic2pro_main)
        communication = threading.Thread(target=self.simpleactions_subscriber.subscription)
        main.start()
        communication.start()

    def set_altitude(self, target):
        self.target_altitude = target
        time.sleep(5)

    def go_forward(self, duration):
        self.pitch_disturbance = 3
        self.yaw_disturbance = 0
        if duration != 0:
            time.sleep(duration)
            self.pitch_disturbance = 0

    def go_backward(self, duration):
        self.pitch_disturbance = -2
        if duration != 0:
            time.sleep(duration)
            self.pitch_disturbance = 0

    def turn_right(self, duration):
        self.yaw_disturbance = 0.5
        if duration != 0:
            time.sleep(duration)
            self.yaw_disturbance = 0

    def turn_left(self, duration):
        self.yaw_disturbance = -0.5
        if duration != 0:
            time.sleep(duration)
            self.yaw_disturbance = 0

    def recognise_objects(self):
        self.recognise = True
        self.camera.recognitionEnable(self.timestep)

    def go_to_location(self, target):
        self.target_loc = target
        self.navigate = True
        while self.navigate:
            time.sleep(1)

    def set_message_target(self, target):
        print(target)
        self.message_recipient = target

    def stop_movement(self):
        self.pitch_disturbance = 0
        self.yaw_disturbance = 0

    def send_location(self):
        if not self.recognise:
            send = threading.Thread(target=self.sync_send_location)
            send.start()
        elif len(self.rec_obj_arr) > self.amount_of_objects:
            self.amount_of_objects = len(self.rec_obj_arr)
            send = threading.Thread(target=self.sync_send_location)
            send.start()
        else:
            print("No recognised object at location")

    # def sync_send_location():
    #     global location
    #     location_json = {"location": [location[0], location[1] - 2]}
    #     requests.post("http://localhost:5002/location", json=location_json)

    def sync_send_location(self):
        location_json = json.dumps({"location": [self.location[0], self.location[1] - 2]})
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        channel = connection.channel()

        channel.exchange_declare(exchange='location_exchange', exchange_type='direct')

        # publish the moose message
        channel.basic_publish(exchange='location_exchange', routing_key=f"{self.message_recipient}_location_queue",
                              body=location_json)
        print(f"[{self.robot_name} sync_send_location] sent location to {self.message_recipient}")
        connection.close()

    # Function that finds the angle and distance to a location and moves the vehicle accordingly
    def navigate_to_location(self):
        global navigate
        global target_loc

        pos = self.gps.getValues()
        north = self.compass.getValues()
        front = [-north[0], north[1], north[2]]
        dir = [self.target_loc[0] - pos[0], self.target_loc[1] - pos[2]]
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

        # stop navigation and vehicle movements when target has been reached
        if distance < 1:
            self.navigate = False
            self.stop_movement()

    def CLAMP(self, value, low, high):
        if value < low:
            return low
        if value > high:
            return high
        return value

    # Function that calculates the values for each motor, keeping the drone stable
    def stabilize_and_control_movement(self):
        roll = self.iu.getRollPitchYaw()[0] + math.pi / 2.0
        pitch = self.iu.getRollPitchYaw()[1]
        roll_acceleration = self.gyro.getValues()[0]
        pitch_acceleration = self.gyro.getValues()[1]
        altitude = self.gps.getValues()[1]

        # Compute the roll, pitch, yaw and vertical inputs.
        roll_input = self.k_roll_p * self.CLAMP(roll, -1.0, 1.0) + \
                     roll_acceleration + self.roll_disturbance
        pitch_input = self.k_pitch_p * \
                      self.CLAMP(pitch, -1.0, 1.0) - pitch_acceleration + self.pitch_disturbance
        yaw_input = self.yaw_disturbance
        clamped_difference_altitude = self.CLAMP(
            self.target_altitude - altitude + self.k_vertical_offset, -1.0, 1.0)
        vertical_input = self.k_vertical_p * pow(clamped_difference_altitude, 3.0)

        # Actuate the motors taking into consideration all the computed inputs.
        front_left_motor_input = self.k_vertical_thrust + \
                                 vertical_input - roll_input - pitch_input + yaw_input
        front_right_motor_input = self.k_vertical_thrust + \
                                  vertical_input + roll_input - pitch_input - yaw_input
        rear_left_motor_input = self.k_vertical_thrust + \
                                vertical_input - roll_input + pitch_input - yaw_input
        rear_right_motor_input = self.k_vertical_thrust + \
                                 vertical_input + roll_input + pitch_input + yaw_input

        # Set the motor velocities required for stabilization and movement
        self.front_left_motor.setVelocity(front_left_motor_input)
        self.front_right_motor.setVelocity(-front_right_motor_input)
        self.rear_left_motor.setVelocity(-rear_left_motor_input)
        self.rear_right_motor.setVelocity(rear_right_motor_input)

    # write the location of this robot to the config file

    def setLocationConfig(self):
        with open('../config.json') as json_data_file:
            data = json.load(json_data_file)

        with open('../config.json', 'w') as json_data_file:
            data['robots']['mavic2pro']['location'] = {
                "x": self.gps.getValues()[0], "y": self.gps.getValues()[2]}
            json.dump(data, json_data_file, indent=2, sort_keys=True)

    # main loop, starting and controlling the robot based on the global variables
    def mavic2pro_main(self):
        step_count = 0
        for motor in self.motors:
            motor.setPosition(float('inf'))

        while self.robot.step(self.timestep) != -1:
            self.location = [self.gps.getValues()[0], self.gps.getValues()[2]]

            if self.navigate:
                self.navigate_to_location()

            self.stabilize_and_control_movement()
            if self.recognise and self.camera.getRecognitionObjects():
                for rec_obj in self.camera.getRecognitionObjects():
                    if rec_obj.id not in self.rec_obj_arr:
                        self.rec_obj_arr.append(rec_obj.id)
                        self.navigate = False
                        self.stop_movement()
            # print(f'(mavic) step number {step_count}')
            step_count += 1
