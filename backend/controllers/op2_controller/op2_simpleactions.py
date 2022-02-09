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
libraryPath = os.path.join(os.environ.get("WEBOTS_HOME"), 'projects', 'robots', 'robotis', 'darwin-op', 'libraries', 'python39')
libraryPath = libraryPath.replace('/', os.sep)
sys.path.append(libraryPath)
from managers import RobotisOp2MotionManager, RobotisOp2GaitManager

# create the Robot instance.
robot = Robot()

# get the time step of the current world.
timestep = int(robot.getBasicTimeStep())

f_up = 0
f_down = 0
gyro = robot.getDevice('Gyro')
gyro.enable(timestep)
x_amplitude_forward = 0.0


positionSensorNames = ['ShoulderR', 'ShoulderL', 'ArmUpperR', 'ArmUpperL',
                                    'ArmLowerR', 'ArmLowerL', 'PelvYR', 'PelvYL',
                                    'PelvR', 'PelvL', 'LegUpperR', 'LegUpperL',
                                    'LegLowerR', 'LegLowerL', 'AnkleR', 'AnkleL',
                                    'FootR', 'FootL', 'Neck', 'Head']

positionSensors = []
for i in range(len(positionSensorNames)):
    positionSensors.append(robot.getDevice(positionSensorNames[i] + 'S'))
    positionSensors[i].enable(timestep)


motion_manager = RobotisOp2MotionManager(robot)
gait_manager = RobotisOp2GaitManager(robot, "")
is_walking = False

target_reached = False
navigate = False
location = []
# simpleactions = ["go_forward(3)", "turn_right(2)", "go_forward(2)"]
simpleactions = []

op2_name = ""

# Initialize which sets the target altitude as well as start the main loop
def init(port, name):
    global op2_name
    op2_name = name
    main = threading.Thread(target=op2_main)
    communication = threading.Thread(target=test_receive_routing_message)
    
    main.start()
    communication.start()

def my_step():
    global robot,timestep
    ret = robot.step(timestep)
    if ret == -1:
        exit(0)
    

def wait(ms):
    global robot
    startTime = robot.getTime()
    sec = ms / 1000
    while sec + startTime >= robot.getTime():
        my_step()


def go_forward(duration):
    global x_amplitude_forward, op2_name
    x_amplitude_forward = 1.0
    if duration != 0:
        print(f"{op2_name} sleeping for {duration} seconds")
        time.sleep(duration)
        x_amplitude_forward = 0.0


def stop_movement():
    global left_speed
    global right_speed
    left_speed = 0
    right_speed = 0



def op2_main():
    global x_amplitude_forward
    step_count = 0
    my_step()       # Simulate a step to refresh the sensor reading
    motion_manager.playPage(9)
    wait(200)

    # Start the gait manager
    gait_manager.start()
    gait_manager.setBalanceEnable(True)

    while robot.step(timestep) != -1:
        gait_manager.setXAmplitude(x_amplitude_forward)
        gait_manager.step(timestep)
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



def test_receive_routing_message():
    global op2_name
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.exchange_declare(exchange='routing_exchange', exchange_type='direct')

    result = channel.queue_declare(queue='', exclusive=True)
    queue_name = result.method.queue

    channel.queue_bind(exchange='routing_exchange', queue=queue_name, routing_key=f"{op2_name}_queue")

    print(f"{op2_name} ready to receive routed messages")
    channel.basic_consume(queue=queue_name, on_message_callback=execute_simpleactions_callback, auto_ack=True)
    
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
