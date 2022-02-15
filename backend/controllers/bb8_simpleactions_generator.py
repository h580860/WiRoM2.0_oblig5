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


class Bb8SimpleactionsGenerator(SimpleactionsSuperclass):
    def __init__(self, name):
        super().__init__(name)

        # initiate the motors
        # keep track of the motors in a dictionary
        self.motors = {}
        self.motor_names = ["body yaw motor", "body pitch motor", "head yaw motor"]
        for name in self.motor_names:
            self.motors[name] = self.robot.getDevice(name)
            self.motors[name].setPosition(float('inf'))
            self.motors[name].setVelocity(0.0)

        self.yaw_speed = 0.0
        self.pitch_speed = 0.0
        self.max_speed = 4.0
        self.attenuation = 0.9

        self.target_reached = False
        self.navigate = False
        self.location = []
        # simpleactions = ["go_forward(3)", "turn_right(2)", "go_forward(2)"]
        self.simpleactions = []

    def initiate_threads(self):
        main = threading.Thread(target=self.bb8_main)
        communication = threading.Thread(target=self.receive_routing_message)
        main.start()
        communication.start()

    def go_forward(self, duration):
        # pitch_speed += attenuation
        self.pitch_speed = self.max_speed

        if duration != 0:
            print(f"{self.robot_name} sleeping for {duration} second(s)")
            time.sleep(duration)
            self.pitch_speed = 0.0

    def go_backward(self, duration):
        # pitch_speed += attenuation
        self.pitch_speed = -self.max_speed

        if duration != 0:
            print(f"{self.robot_name} sleeping for {duration} second(s)")
            time.sleep(duration)
            self.pitch_speed = 0.0

    def turn_left(self, duration):
        self.yaw_speed = self.max_speed

        if duration != 0:
            time.sleep(duration)
            self.yaw_speed = 0

    def turn_right(self, duration):
        self.yaw_speed = -self.max_speed

        if duration != 0:
            time.sleep(duration)
            self.yaw_speed = 0

    def bb8_main(self):
        step_count = 0

        while self.robot.step(self.timestep) != -1:
            # pitch_speed = min(max_speed, max(-max_speed, attenuation * pitch_speed))
            # yaw_speed = min(max_speed, max(-max_speed, attenuation * yaw_speed))
            self.motors['body yaw motor'].setVelocity(self.yaw_speed)
            self.motors['head yaw motor'].setVelocity(self.yaw_speed)
            self.motors['body pitch motor'].setVelocity(self.pitch_speed)
            step_count += 1
