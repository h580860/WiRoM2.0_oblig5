"""
PR2 controller
Source: https://github.com/cyberbotics/webots/blob/released/projects/robots/clearpath/pr2/controllers/pr2_demo/pr2_demo.c
"""

# You may need to import some classes of the controller module. Ex:
#  from controller import Robot, Motor, DistanceSensor
from controller import Robot, Motor

# create the Robot instance.
robot = Robot()

# get the time step of the current world.
timestep = int(robot.getBasicTimeStep())

# define variables
max_wheel_speed = 3.0           # maximum velocity for the wheels [rad / s]
# distance between 2 caster wheels (the four wheels are located in square) [m]
wheels_distance = 0.4492
# distance between 2 sub wheels of a caster wheel [m]
sub_wheels_distance = 0.098
wheel_radius = 0.08             # wheel radius

# ------------------------------------------------------------------------
# Initiate the devices

# list of device names
wheel_names = ["FLL_WHEEL", "FLR_WHEEL", "FRL_WHEEL",
               "FRR_WHEEL", "BLL_WHEEL", "BLR_WHEEL", "BRL_WHEEL", "BRR_WHEEL"]
wheel_device_names = ["fl_caster_l_wheel_joint", "fl_caster_r_wheel_joint",
                      "fr_caster_l_wheel_joint", "fr_caster_r_wheel_joint", "bl_caster_l_wheel_joint", "bl_caster_r_wheel_joint", "br_caster_l_wheel_joint", "br_caster_r_wheel_joint"]

rotation_names = ["FL_ROTATION", "FR_ROTATION", "BL_ROTATION", "BR_ROTATION"]
roll_names = ["SHOULDER_ROLL", "SHOULDER_LIFT",
              "UPPER_ARM_ROLL", "ELBOW_LIFT", "WRIST_ROLL"]
finger_names = ["LEFT_FINGER, RIGHT_FINGER, LEFT_TIP, RIGHT_TIP"]


# Both get and set the positions and velocity
wheel_motors = {}
for i in range(8):
    curr_name = wheel_names[i]
    wheel_motors[curr_name] = robot.getDevice(wheel_device_names[i])
    wheel_motors[curr_name].setPosition(float('inf'))
    wheel_motors[curr_name].setVelocity(0.0)
# ------------------------------------------------------------------------
# Enable the devices


# ------------------------------------------------------------------------

# Main loop:
# - perform simulation steps until Webots is stopping the controller
while robot.step(timestep) != -1:
    # Read the sensors:
    # Enter here functions to read sensor data, like:
    #  val = ds.getValue()

    # Process sensor data here.
    for i in range(8):
        curr_name = wheel_names[i]
        wheel_motors[curr_name].setVelocity(max_wheel_speed)

    # Enter here functions to send actuator commands, like:
    #  motor.setPosition(10.0)
    pass

# Enter here exit cleanup code.
