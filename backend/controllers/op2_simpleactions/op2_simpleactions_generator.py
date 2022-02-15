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


class Op2SimpleactionsGenerator:
    def __init__(self, name):
        # create the Robot instance.
        self.robot = Robot()
        self.robot_name = name

        # get the time step of the current world.
        self.timestep = int(self.robot.getBasicTimeStep())

        self.fup = 0
        self.fdown = 0
        self.gyro = self.robot.getDevice('Gyro')
        self.gyro.enable(self.timestep)
        self.accelerometer = self.robot.getDevice('Accelerometer')
        self.accelerometer.enable(self.timestep)
        self.x_amplitude_forward = 0.0

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
        # simpleactions = ["go_forward(3)", "turn_right(2)", "go_forward(2)"]
        self.simpleactions = []

    # Initialize which sets the target altitude as well as start the main loop
    def initiate_threads(self):
        main = threading.Thread(target=self.op2_main)
        communication = threading.Thread(target=self.receive_routing_message)
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

            self.gait_manager.setXAmplitude(self.x_amplitude_forward)
            self.gait_manager.step(self.timestep)
            step_count += 1

    def execute_simpleactions(self):
        try:
            while True:
                if self.simpleactions:
                    simpleaction = self.simpleactions.pop(0)
                    print("Executing simpleaction " + simpleaction)
                    eval(f'self.{simpleaction}')
                else:
                    print("No available simpleaction")
        except Exception as e:
            print(e)

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
            eval(f'self.{sim_act}')
        print("finished callback function")
