"""mavic2pro_controller simpleactions."""
from controller import Robot, Motor, PositionSensor, Gyro, Camera, InertialUnit, GPS, Compass, CameraRecognitionObject
# from flask import Flask, request
import requests
import math
import threading
import time
import json
# from ... import Wirom_logger
# from Logs.wirom_logger import Wirom_logger
import sys
import os
# sys.path.insert(0, os.path.join(os.getcwd(), os.pardir, os.pardir))
# from backend.wirom_logger import Wirom_logge
import logging
import pika


# create flask instance
# app = Flask(__name__)
# app.debug = True


class mavic2pro_simpleactions(port):
    def __init__(self, port):

        # configure logging 
        # wirom_logger = Wirom_logger("mavic2pro.log")
        logging.basicConfig(format='%(asctime)s %(message)s', filename=os.path.join(
            os.pardir, os.pardir, "mavic2pro.log"), encoding='utf-8', level=logging.DEBUG)
        logging.info("-" * 50)

        # create the Robot instance.
        self.robot = Robot()

        # get the time step of the current world.
        self.timestep = int(self.robot.getBasicTimeStep())

        # get the motors for the robot
        self.front_left_motor = self.robot.getDevice('front left propeller')
        self.front_right_motor = self.robot.getDevice('front right propeller')
        self.rear_left_motor = self.robot.getDevice('rear left propeller')
        self.rear_right_motor = self.robot.getDevice('rear right propeller')
        self.motors = [self.front_left_motor, self.front_right_motor,
                self.rear_left_motor, self.rear_right_motor]

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
        self.k_vertical_p = 3.0        # P constant of the vertical PID.
        self.k_roll_p = 50.0           # P constant of the roll PID.
        self.k_pitch_p = 30.0          # P constant of the pitch PID.

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

    
        self.init_threads(port)


    def init(self, port):
        # Initialize which sets the target altitude as well as start the main loop
        logging.info("init")
        self.main = threading.Thread(target=self.mavic2pro_main)
        # execute = threading.Thread(target=execute_simpleactions)
        # communication = threading.Thread(target=test_communcation_receive)
        self.communication = threading.Thread(target=self.test_receive_routing_message)
        self.main.start()
        # execute.start()
        self.communication.start()
        # app.run(port=port)'


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
        channel.basic_publish(exchange='location_exchange', routing_key= self.message_recipient+'_location_queue', body=location_json)
        print("[mavic sync_send_location] sent location to " + self.message_recipient)
        connection.close()


    # Function that finds the angle and distance to a location and moves the vehicle accordingly
    def navigate_to_location(self):
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
            navigate = False
            self.stop_movement()
            
        # TODO GOT HERE!!! 15.11.2021 15:48


    def CLAMP(value, low, high):
        if value < low:
            return low
        if value > high:
            return high
        return value


    # Function that calculates the values for each motor, keeping the drone stable
    def stabilize_and_control_movement():
        roll = iu.getRollPitchYaw()[0] + math.pi / 2.0
        pitch = iu.getRollPitchYaw()[1]
        roll_acceleration = gyro.getValues()[0]
        pitch_acceleration = gyro.getValues()[1]
        altitude = gps.getValues()[1]

        # Compute the roll, pitch, yaw and vertical inputs.
        roll_input = k_roll_p * CLAMP(roll, -1.0, 1.0) + \
            roll_acceleration + roll_disturbance
        pitch_input = k_pitch_p * \
            CLAMP(pitch, -1.0, 1.0) - pitch_acceleration + pitch_disturbance
        yaw_input = yaw_disturbance
        clamped_difference_altitude = CLAMP(
            target_altitude - altitude + k_vertical_offset, -1.0, 1.0)
        vertical_input = k_vertical_p * pow(clamped_difference_altitude, 3.0)

        # Actuate the motors taking into consideration all the computed inputs.
        front_left_motor_input = k_vertical_thrust + \
            vertical_input - roll_input - pitch_input + yaw_input
        front_right_motor_input = k_vertical_thrust + \
            vertical_input + roll_input - pitch_input - yaw_input
        rear_left_motor_input = k_vertical_thrust + \
            vertical_input - roll_input + pitch_input - yaw_input
        rear_right_motor_input = k_vertical_thrust + \
            vertical_input + roll_input + pitch_input + yaw_input

        # Set the motor velocities required for stabilization and movement
        front_left_motor.setVelocity(front_left_motor_input)
        front_right_motor.setVelocity(-front_right_motor_input)
        rear_left_motor.setVelocity(-rear_left_motor_input)
        rear_right_motor.setVelocity(rear_right_motor_input)

    # write the location of this robot to the config file


    def setLocationConfig():
        with open('../config.json') as json_data_file:
            data = json.load(json_data_file)

        with open('../config.json', 'w') as json_data_file:
            data['robots']['mavic2pro']['location'] = {
                "x": gps.getValues()[0], "y": gps.getValues()[2]}
            json.dump(data, json_data_file, indent=2, sort_keys=True)


    # main loop, starting and controlling the robot based on the global variables
    def mavic2pro_main():
        global recognise
        global navigate
        global rec_obj_arr
        global location

        logging.info("maciv2pro_main")
        step_count = 0

        for motor in motors:
            motor.setPosition(float('inf'))

        while robot.step(timestep) != -1:
            location = [gps.getValues()[0], gps.getValues()[2]]

            if navigate:
                navigate_to_location()

            stabilize_and_control_movement()
            if recognise and camera.getRecognitionObjects():
                for rec_obj in camera.getRecognitionObjects():
                    if rec_obj.id not in rec_obj_arr:
                        rec_obj_arr.append(rec_obj.id)
                        navigate = False
                        stop_movement()
            # print(f'(mavic) step number {step_count}')
            step_count += 1


    # Function for receiving simpleactions from server
    # @app.route('/simpleactions', methods=['POST'])
    # def receive_simpleactions():
    #     global simpleactions
    #     logging.info("receive_location")
    #     simpleactions = request.get_json()
    #     return "Updated simple actions", 200

    # Function for executing simpleactions in the queue
    def execute_simpleactions():
        global simpleactions
        logging.info("receive_simpleactions")

        while robot.step(timestep) != -1:
            if simpleactions:
                simpleaction = simpleactions.pop(0)
                print('Executing simpleaction: ' + simpleaction)
                eval(simpleaction)


    def test_communcation_receive():
        # initiate messaging communication
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))
        channel = connection.channel()
        channel.exchange_declare(exchange='test_exchange', exchange_type='fanout')

        result = channel.queue_declare(queue='', exclusive=True)
        queue_name = result.method.queue

        channel.queue_bind(exchange='test_exchange', queue=queue_name)

        print("Mavic2Pro ready to receive messages")

        channel.basic_consume(
            queue=queue_name, on_message_callback=execute_simpleactions_callback, auto_ack=True)
        channel.start_consuming()



    def test_receive_routing_message():
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))
        channel = connection.channel()
        channel.exchange_declare(
            exchange='routing_exchange', exchange_type='direct')

        result = channel.queue_declare(queue='', exclusive=True)
        queue_name = result.method.queue

        channel.queue_bind(exchange='routing_exchange', queue=queue_name, routing_key="mavic_queue")

        print("Mavic ready to receive routed messages")
        channel.basic_consume(
            queue=queue_name,
            on_message_callback=execute_simpleactions_callback,
            auto_ack=True
            )
        
        channel.start_consuming()



    def execute_simpleactions_callback(ch, method, properties, body):
        global simpleactions
        print("(mavic2pro) callback: %r" % body)
        # TODO as for now, the incoming messages are functions calls, separated by ","
        # simpleactions.extend(body.decode('utf-8').split(","))
        # simpleactions.extend(body.decode('utf-8'))


        new_simpleactions = json.loads(body.decode('utf-8'))
        simpleactions.extend(new_simpleactions)
        print(f'(mavic) Simpleactions = {simpleactions}, type={type(simpleactions)}')


        # Now execute the simpleactions
        # for i in range(len(simpleactions)):
        while simpleactions:
            sim_act = simpleactions.pop(0)
            print("(mavic) Executing simpleaction " + sim_act)
            eval(sim_act)
        print("finished callback function")



    def callback(ch, method, properties, body):
        print("(mavic2pro) %r" % body)
        logging.info("(mavic2pro) %r" % body)