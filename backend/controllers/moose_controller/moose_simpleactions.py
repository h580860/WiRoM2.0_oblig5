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


# from backend.wirom_logger import Wirom_logger
logging.basicConfig(format='%(asctime)s %(message)s', filename=os.path.join(os.pardir, os.pardir, "moose.log"), encoding='utf-8', level=logging.DEBUG)
logging.info("-" * 50)


# create flask instance
# app = Flask(__name__)
# app.debug = True

# configure logging
# wirom_logger = Wirom_logger("moose.log")


# create the Robot instance.
robot = Robot()

# get the time step of the current world.
timestep = int(robot.getBasicTimeStep())

left_motor_names = ["left motor 1",  "left motor 2",
                    "left motor 3",  "left motor 4"]
right_motor_names = ["right motor 1",
                     "right motor 2", "right motor 3", "right motor 4"]
left_motors = [robot.getDevice(name) for name in left_motor_names]
right_motors = [robot.getDevice(name) for name in right_motor_names]
left_speed = 0
right_speed = 0

# get and enable nodes used by the robot
gps = robot.getDevice('gps')
compass = robot.getDevice('compass')
gps.enable(timestep)
compass.enable(timestep)

target_reached = False
navigate = False
location = []
# simpleactions = ["go_forward(3)", "turn_right(2)", "go_forward(2)"]
simpleactions = []

# Initialize which sets the target altitude as well as start the main loop
def init(port):
    logging.info("init")
    print("before")
    main = threading.Thread(target=moose_main)
    # execute = threading.Thread(target=execute_simpleactions)
    # communication = threading.Thread(target=test_communcation_receive)
    communication = threading.Thread(target=test_receive_routing_message)
    location_communication = threading.Thread(target=test_receive_location)

    print("after")
    main.start()
    # execute.start()
    communication.start()
    location_communication.start()
    # app.run(port=port)


def go_forward(duration):
    global left_speed
    global right_speed
    left_speed = 7.0
    right_speed = 7.0
    if duration != 0:
        print(f"Moose sleeping for {duration} seconds")
        time.sleep(duration)
        left_speed = 0
        right_speed = 0


def go_backward(duration):
    global left_speed
    global right_speed
    left_speed = -2.0
    right_speed = -2.0
    if duration != 0:
        time.sleep(duration)
        left_speed = 0
        right_speed = 0


def turn_left(duration):
    global left_speed
    global right_speed
    left_speed = 1.0
    right_speed = 4.0
    if duration != 0:
        time.sleep(duration)
        left_speed = 0
        right_speed = 0


def turn_right(duration):
    global left_speed
    global right_speed
    left_speed = 4.0
    right_speed = 1.0
    if duration != 0:
        time.sleep(duration)
        left_speed = 0
        right_speed = 0


def go_to_location(target):
    global location
    global navigate
    if not location and target:
        location = [target]

    navigate = True
    while navigate:
        time.sleep(1)


def stop_movement():
    global left_speed
    global right_speed
    left_speed = 0
    right_speed = 0

# Function that finds the angle and distance to a location and moves the vehicle accordingly
def navigate_to_location():
    global navigate
    global location
    loc = location[0]

    pos = gps.getValues()
    north = compass.getValues()
    front = [-north[0], north[1], north[2]]

    dir = [loc[0] - pos[0], loc[1] - pos[2]]
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

    # stop vehicle and navigation when target has been reached
    if distance < 1:
        print('Reached target')
        navigate = False
        location.pop(0)
        stop_movement()

#Actively wait for new location
def receive_location_from_robot():
    while not location:
        time.sleep(1)

# write the location of this robot to the config file
def setLocationConfig():
    with open('../config.json') as json_data_file:
        data = json.load(json_data_file)

    with open('../config.json', 'w') as json_data_file:
        data['robots']['moose']['location'] = {
            "x": gps.getValues()[0], "y": gps.getValues()[2]}
        json.dump(data, json_data_file, indent=2, sort_keys=True)


def moose_main():
    logging.info("moose_main")
    step_count = 0
    for motor in left_motors:
        motor.setPosition(float('inf'))
    for motor in right_motors:
        motor.setPosition(float('inf'))

    while robot.step(timestep) != -1:
        if navigate:
            navigate_to_location()
        for motor in left_motors:
            motor.setVelocity(left_speed)
        for motor in right_motors:
            motor.setVelocity(right_speed)
        # print(f'(moose) step number {step_count}')
        step_count += 1
        # logging.info(step_count)
        # print("main iteration")



# # Function for receiving messages from other robots
# @app.route('/location', methods=['POST'])
# def receive_location():
#     global location
#     logging.info("receive_location")
#     msg = request.get_json()
#     location.append(msg['location'])
#     return "Received location", 200


# # Function for receiving simpleactions from server
# @app.route('/simpleactions', methods=['POST'])
# def receive_simpleactions():
#     global simpleactions
#     logging.info("receive_simpleactions")
#     simpleactions = request.get_json()
#     return "Updated simple actions", 200


# Function for executing simpleactions in the queue
# def execute_simpleactions():
#     global simpleactions
#     try:
#         while robot.step(timestep) != -1:
#             if simpleactions:
#                 simpleaction = simpleactions.pop(0)
#                 print('Executing simpleaction: ' + simpleaction)
#                 eval(simpleaction)
#             # else:
#                 # logging.info("No more simpleactions")
#                 # print("No more simpleactions")
#     except Exception as e:
#             print(e)
#     print(f'robot step = {robot.step(timestep)}')


def execute_simpleactions():
    global simpleactions
    try:
        while True:
            if simpleactions:
                    simpleaction = simpleactions.pop(0)
                    print("Executing simpleaction " + simpleaction)
                    eval(simpleaction)
            else:
                print("No available simpleaction")
    except Exception as e:
        print(e)



def test_communcation_receive():
     # initiate messaging communication
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.exchange_declare(exchange='test_exchange', exchange_type='fanout')

    result = channel.queue_declare(queue='', exclusive=True)
    queue_name = result.method.queue

    channel.queue_bind(exchange='test_exchange', queue=queue_name)

    print("Moose ready to receive messages")

    channel.basic_consume(queue=queue_name, on_message_callback=execute_simpleactions_callback, auto_ack=True)
    channel.start_consuming()


def test_receive_routing_message():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.exchange_declare(exchange='routing_exchange', exchange_type='direct')

    result = channel.queue_declare(queue='', exclusive=True)
    queue_name = result.method.queue

    channel.queue_bind(exchange='routing_exchange', queue=queue_name, routing_key="moose_queue")

    print("Moose ready to receive routed messages")
    channel.basic_consume(queue=queue_name, on_message_callback=execute_simpleactions_callback, auto_ack=True)
    
    channel.start_consuming()


def test_receive_location():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.exchange_declare(exchange='location_exchange', exchange_type='direct')

    result = channel.queue_declare(queue='', exclusive=True)
    queue_name = result.method.queue

    channel.queue_bind(exchange='location_exchange', queue=queue_name, routing_key="moose_location_queue")

    print("Moose ready to receive locations")
    channel.basic_consume(queue=queue_name, on_message_callback=receive_location_callback, auto_ack=True)
    channel.start_consuming()



def execute_simpleactions_callback(ch, method, properties, body):
    global simpleactions
    print("(moose) callback: %r" % body)
    # TODO as for now, the incoming messages are functions calls, separated by ","
    # simpleactions.extend(body.decode('utf-8').split(","))

    # Decode the JSON back to a list
    new_simpleactions = json.loads(body.decode('utf-8'))
    simpleactions.extend(new_simpleactions)
    print(f'(moose) Simpleactions = {simpleactions}, type={type(simpleactions)}')
    
    # Now execute the simpleactions
    # for i in range(len(simpleactions)):
    while simpleactions:
        sim_act = simpleactions.pop(0)
        print("(moose) Executing simpleaction " + sim_act)
        eval(sim_act)
    print("finished callback function")


def receive_location_callback(ch, method, properties, body):
    global location
    print("(moose) received locations")

    new_location = json.loads(body.decode('utf-8'))
    # print(f"new location={new_location}, type = {type(new_location)}")
    location.append(new_location['location'])



def callback(ch, method, properties, body):
    print("(moose) %r" % body)
    # logging.info("(moose) %r" % body)
    print("(moose print)" + str(body))
    print(body.decode('UTF-8'))
