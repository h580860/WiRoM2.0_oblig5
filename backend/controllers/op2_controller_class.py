"""op2_controller simpleactions."""
""" Source: http://www.running-robot.net/en/notice-en/212.html """
import math
import threading
import time
import json
import pika
from controller import Robot
# TODO fix the LEDS
# from controller import LED
import os
import sys

libraryPath = os.path.join(os.environ.get("WEBOTS_HOME"), 'projects', 'robots', 'robotis', 'darwin-op', 'libraries',
                           'python39')
libraryPath = libraryPath.replace('/', os.sep)
sys.path.append(libraryPath)
from managers import RobotisOp2MotionManager, RobotisOp2GaitManager
from controller_superclass import ControllerSuperclass


class Op2ControllerClass(ControllerSuperclass):
    def __init__(self, name):
        super().__init__(name, "op2")

        self.fup = 0
        self.fdown = 0
        self.gyro = self.robot.getDevice('Gyro')
        self.gyro.enable(self.timestep)
        self.accelerometer = self.robot.getDevice('Accelerometer')
        self.accelerometer.enable(self.timestep)
        self.x_amplitude_forward = 0.0
        self.a_amplitude_sideways = 0.0
        self.left_speed = 0
        self.right_speed = 0

        self.positionSensorNames = ['ShoulderR', 'ShoulderL', 'ArmUpperR', 'ArmUpperL',
                                    'ArmLowerR', 'ArmLowerL', 'PelvYR', 'PelvYL',
                                    'PelvR', 'PelvL', 'LegUpperR', 'LegUpperL',
                                    'LegLowerR', 'LegLowerL', 'AnkleR', 'AnkleL',
                                    'FootR', 'FootL', 'Neck', 'Head']

        self.positionSensors = []
        for i in range(len(self.positionSensorNames)):
            self.positionSensors.append(self.robot.getDevice(self.positionSensorNames[i] + 'S'))
            self.positionSensors[i].enable(self.timestep)

        self.motion_manager = RobotisOp2MotionManager(self.robot)
        self.gait_manager = RobotisOp2GaitManager(self.robot, "")
        self.is_walking = False

        self.target_reached = False
        self.navigate = False
        self.location = []
        self.is_turning = False

        self.add_all_simpleactions()

    def add_all_simpleactions(self):
        self.add_available_simpleaction("go_forward", self.go_forward)
        self.add_available_simpleaction("go_backward", self.go_backwards)
        self.add_available_simpleaction("turn_right", self.turn_right)
        self.add_available_simpleaction("turn_left", self.turn_left)

    # Initialize which sets the target altitude as well as start the main loop
    def initiate_threads(self):
        main = threading.Thread(target=self.op2_main)
        communication = threading.Thread(target=self.simpleactions_subscriber.subscription)
        main.start()
        communication.start()

    # Source: https://github.com/cyberbotics/webots/blob/released/projects/robots/robotis/darwin-op/controllers/walk/Walk.cpp
    def check_if_fallen(self):
        global accelerometer, motion_manager, op2_name, fup, fdown
        accelerometer_tolerance = 80.0
        accelerometer_step = 100

        # Count how many steps the accelerometer says the robot is down
        accelerometer_values = self.accelerometer.getValues()
        if accelerometer_values[1] < 520.0 - accelerometer_tolerance:
            self.fup += 1
        else:
            self.fup = 0

        if accelerometer_values[1] > 512.0 + accelerometer_tolerance:
            self.fdown += 1
        else:
            self.fdown = 0

        # the robot is face down
        if self.fup > accelerometer_step:
            self.motion_manager.playPage(10)
            self.motion_manager.playPage(9)
            self.fup = 0
            print(f"{self.robot_name} is face down")
        elif self.fdown > accelerometer_step:
            self.motion_manager.playPage(11)
            self.motion_manager.playPage(9)
            self.fdown = 0
            print(f"{self.robot_name} is face up")

    def my_step(self):
        ret = self.robot.step(self.timestep)
        if ret == -1:
            exit(0)

    def wait(self, ms):
        startTime = self.robot.getTime()
        sec = ms / 1000
        while sec + startTime >= self.robot.getTime():
            self.my_step()

    def go_forward(self, duration):
        self.x_amplitude_forward = 1.0
        if duration != 0:
            print(f"{self.robot_name} sleeping for {duration} seconds")
            time.sleep(duration)
            self.x_amplitude_forward = 0.0

    def go_backwards(self, duration): 
        self.x_amplitude_forward = -1.0
        if duration != 0:
            time.sleep(duration)
            self.x_amplitude_forward = 0.0
    
    def turn_right(self, duration):
        self.a_amplitude_sideways = -0.5 
        if duration != 0:
            time.sleep(duration)
            self.a_amplitude_sideways = 0.0

    def turn_left(self, duration):
        self.a_amplitude_sideways = 0.5 
        if duration != 0:
            time.sleep(duration)
            self.a_amplitude_sideways = 0.0


    def stop_movement(self):
        self.left_speed = 0
        self.right_speed = 0

    def op2_main(self):
        step_count = 0
        self.my_step()  # Simulate a step to refresh the sensor reading
        self.motion_manager.playPage(9)
        self.wait(200)

        # Start the gait manager
        self.gait_manager.start()
        self.gait_manager.setBalanceEnable(True)

        while self.robot.step(self.timestep) != -1:
            self.check_if_fallen()

            # if self.is_turning:
            #     self.gait_manager.setXAmplitude
            #     self.gait_manager.setAAmplitude(self.a_amplitude_sideways)
            # else:
            self.gait_manager.setAAmplitude(self.a_amplitude_sideways)
            self.gait_manager.setXAmplitude(self.x_amplitude_forward)
            self.gait_manager.step(self.timestep)
            step_count += 1