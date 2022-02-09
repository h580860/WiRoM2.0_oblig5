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

# create the Robot instance.
robot = Robot()

# get the time step of the current world.
timestep = int(robot.getBasicTimeStep())

# initiate the motors
# keep track of the motors in a dictionary
motors = {}
motor_names = ["body yaw motor", "body pitch motor", "head yaw motor"]
for name in motor_names:
    motors[name] = robot.getDevice(name)
    motors[name].setPosition(float('inf'))
    motors[name].setVelocity(0.0)

yaw_speed = 0.0
pitch_speed = 0.0
max_speed = 4.0
attenuation = 0.9

target_reached = False
navigate = False
location = []
# simpleactions = ["go_forward(3)", "turn_right(2)", "go_forward(2)"]
simpleactions = []

bb8_name = ""


# Initialize which sets the target altitude as well as start the main loop
def init(port, name):
    global bb8_name
    logging.info("init")
    bb8_name = name
    main = threading.Thread(target=bb8_main)
    communication = threading.Thread(target=receive_routing_message)
    main.start()
    communication.start()

def go_forward(duration):
    global pitch_speed, attenuation, bb8_name, max_speed
    # pitch_speed += attenuation
    pitch_speed = max_speed

    if duration != 0:
        print(f"{bb8_name} sleeping for {duration} second(s)")
        time.sleep(duration)
        pitch_speed = 0.0


def go_backward(duration):
    global pitch_speed, attenuation, bb8_name, max_speed
    # pitch_speed += attenuation
    pitch_speed = -max_speed

    if duration != 0:
        print(f"{bb8_name} sleeping for {duration} second(s)")
        time.sleep(duration)
        pitch_speed = 0.0

def turn_left(duration):
    global yaw_speed, max_speed
    yaw_speed = max_speed

    if duration != 0:
        time.sleep(duration)
        yaw_speed = 0


def turn_right(duration):
    global yaw_speed, max_speed
    yaw_speed = -max_speed

    if duration != 0:
        time.sleep(duration)
        yaw_speed = 0


def bb8_main():
    global yaw_speed, pitch_speed, max_speed
    step_count = 0

    while robot.step(timestep) != -1:
        # pitch_speed = min(max_speed, max(-max_speed, attenuation * pitch_speed))
        # yaw_speed = min(max_speed, max(-max_speed, attenuation * yaw_speed))
        motors['body yaw motor'].setVelocity(yaw_speed)
        motors['head yaw motor'].setVelocity(yaw_speed)
        motors['body pitch motor'].setVelocity(pitch_speed)
        step_count += 1


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


def receive_routing_message():
    global bb8_name
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.exchange_declare(exchange='routing_exchange', exchange_type='direct')

    result = channel.queue_declare(queue='', exclusive=True)
    queue_name = result.method.queue

    channel.queue_bind(exchange='routing_exchange', queue=queue_name, routing_key=f"{bb8_name}_queue")

    print(f"{bb8_name} ready to receive routed messages")
    channel.basic_consume(queue=queue_name, on_message_callback=execute_simpleactions_callback, auto_ack=True)

    channel.start_consuming()


def execute_simpleactions_callback(ch, method, properties, body):
    global simpleactions, bb8_name
    print(f"{bb8_name} callback: %r" % body)
    # TODO as for now, the incoming messages are functions calls, separated by ","
    # simpleactions.extend(body.decode('utf-8').split(","))

    # Decode the JSON back to a list
    new_simpleactions = json.loads(body.decode('utf-8'))
    simpleactions.extend(new_simpleactions)
    print(f'{bb8_name} Simpleactions = {simpleactions}, type={type(simpleactions)}')

    # Now execute the simpleactions
    # for i in range(len(simpleactions)):
    while simpleactions:
        sim_act = simpleactions.pop(0)
        print(f"{bb8_name} Executing simpleaction " + sim_act)
        eval(sim_act)
    print("finished callback function")
