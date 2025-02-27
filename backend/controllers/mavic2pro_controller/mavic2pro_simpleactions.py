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

# configure logging
# wirom_logger = Wirom_logger("mavic2pro.log")
# logging.basicConfig(format='%(asctime)s %(message)s', filename=os.path.join(
#     os.pardir, os.pardir, "mavic2pro.log"), encoding='utf-8', level=logging.DEBUG)
# logging.info("-" * 50)

# create the Robot instance.
robot = Robot()

# get the time step of the current world.
timestep = int(robot.getBasicTimeStep())

# get the motors for the robot
front_left_motor = robot.getDevice('front left propeller')
front_right_motor = robot.getDevice('front right propeller')
rear_left_motor = robot.getDevice('rear left propeller')
rear_right_motor = robot.getDevice('rear right propeller')
motors = [front_left_motor, front_right_motor,
          rear_left_motor, rear_right_motor]

# get and enable nodes used by the robot
gyro = robot.getDevice('gyro')
iu = robot.getDevice('inertial unit')
gps = robot.getDevice('gps')
compass = robot.getDevice('compass')
camera = robot.getDevice('camera')

gyro.enable(timestep)
iu.enable(timestep)
gps.enable(timestep)
compass.enable(timestep)
camera.enable(timestep)

# empirically found constants for the drone to perform stable flight; inspired by the drone demo controller
k_vertical_thrust = 68.5  # with this thrust, the drone lifts.
# Vertical offset where the robot actually targets to stabilize itself.
k_vertical_offset = 0.6
k_vertical_p = 3.0  # P constant of the vertical PID.
k_roll_p = 50.0  # P constant of the roll PID.
k_pitch_p = 30.0  # P constant of the pitch PID.

# variables that control the movement of the drone
target_altitude = 0
roll_disturbance = 0
pitch_disturbance = 0
yaw_disturbance = 0

# variables to set drone functions
rec_obj_arr = []
recognise = False
navigate = False
target_reached = False
message_recipient = ''
location = []
target_loc = []
simpleactions = []
amount_of_objects = 0

mavic_name = ""


# Initialize which sets the target altitude as well as start the main loop
def init(port, name):
    global mavic_name
    logging.info("init")
    mavic_name = name
    main = threading.Thread(target=mavic2pro_main)
    # execute = threading.Thread(target=execute_simpleactions)
    # communication = threading.Thread(target=test_communcation_receive)
    communication = threading.Thread(target=test_receive_routing_message)
    main.start()
    # execute.start()
    communication.start()
    # app.run(port=port)'


def set_altitude(target):
    global target_altitude
    target_altitude = target
    time.sleep(5)


def go_forward(duration):
    global pitch_disturbance
    global yaw_disturbance
    pitch_disturbance = 3
    yaw_disturbance = 0
    if duration != 0:
        time.sleep(duration)
        pitch_disturbance = 0


def go_backward(duration):
    global pitch_disturbance
    pitch_disturbance = -2
    if duration != 0:
        time.sleep(duration)
        pitch_disturbance = 0


def turn_right(duration):
    global yaw_disturbance
    yaw_disturbance = 0.5
    if duration != 0:
        time.sleep(duration)
        yaw_disturbance = 0


def turn_left(duration):
    global yaw_disturbance
    yaw_disturbance = -0.5
    if duration != 0:
        time.sleep(duration)
        yaw_disturbance = 0


def recognise_objects():
    global recognise
    recognise = True
    camera.recognitionEnable(timestep)


def go_to_location(target):
    global target_loc
    global navigate
    target_loc = target
    navigate = True
    while navigate:
        time.sleep(1)


def set_message_target(target):
    print(target)
    global message_recipient
    message_recipient = target


def stop_movement():
    global pitch_disturbance
    global yaw_disturbance
    pitch_disturbance = 0
    yaw_disturbance = 0


def send_location():
    global amount_of_objects
    if not recognise:
        send = threading.Thread(target=sync_send_location)
        send.start()
    elif len(rec_obj_arr) > amount_of_objects:
        amount_of_objects = len(rec_obj_arr)
        send = threading.Thread(target=sync_send_location)
        send.start()
    else:
        print("No recognised object at location")


# def sync_send_location():
#     global location
#     location_json = {"location": [location[0], location[1] - 2]}
#     requests.post("http://localhost:5002/location", json=location_json)

def sync_send_location():
    global location
    location_json = json.dumps({"location": [location[0], location[1] - 2]})
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.exchange_declare(exchange='location_exchange', exchange_type='direct')

    # publish the moose message
    channel.basic_publish(exchange='location_exchange', routing_key=message_recipient + '_location_queue',
                          body=location_json)
    print("[mavic sync_send_location] sent location to " + message_recipient)
    connection.close()


# Function that finds the angle and distance to a location and moves the vehicle accordingly
def navigate_to_location():
    global navigate
    global target_loc

    pos = gps.getValues()
    north = compass.getValues()
    front = [-north[0], north[1], north[2]]
    dir = [target_loc[0] - pos[0], target_loc[1] - pos[2]]
    distance = math.sqrt(dir[0] * dir[0] + dir[1] * dir[1])

    # calculate the angle of which the vehicle is supposed to go to reach target
    angle = math.atan2(dir[1], dir[0]) - math.atan2(front[2], front[0])
    if angle < 0:
        angle += 2 * math.pi

    # vehicle is on the right path when angle = math.pi
    if angle < math.pi - 0.01:
        turn_left(0)
    elif angle > math.pi + 0.01:
        turn_right(0)
    else:
        go_forward(0)

    # stop navigation and vehicle movements when target has been reached
    if distance < 1:
        navigate = False
        stop_movement()


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
    print("")

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
    global mavic_name
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.exchange_declare(
        exchange='routing_exchange', exchange_type='direct')

    result = channel.queue_declare(queue='', exclusive=True)
    queue_name = result.method.queue

    channel.queue_bind(exchange='routing_exchange', queue=queue_name, routing_key=f"{mavic_name}_queue")

    print(f"{mavic_name} ready to receive routed messages")
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
    print(f"(mavic2pro) finished callback function")


def callback(ch, method, properties, body):
    print("(mavic2pro) %r" % body)
    logging.info("(mavic2pro) %r" % body)
