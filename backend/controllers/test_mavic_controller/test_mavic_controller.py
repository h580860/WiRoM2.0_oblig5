"""test_mavic_controller controller."""
# You may need to import some classes of the controller module. Ex:
#  from controller import Robot, Motor, DistanceSensor
from controller import Robot, Keyboard
import math


def CLAMP(value, low, high):
    if value < low:
        return low
    if value > high:
        return high
    return value


# create the Robot instance.
robot = Robot()

# get the time step of the current world.
timestep = int(robot.getBasicTimeStep())

# Get and enable the devices
# TODO add camera roll and camera pitch
devices_dict = {}
device_names = ["camera", "inertial unit", "gps", "compass", "gyro"]
for name in device_names:
    device = robot.getDevice(name)
    device.enable(timestep)
    devices_dict[name] = device


# Enable the keyboard
keyboard = Keyboard()
keyboard.enable(timestep)


# get the motors for the robot
motor_dict = {}
motor_names = ["front left propeller", "front right propeller", "rear left propeller", "rear right propeller"]
for name in motor_names:
    motor = robot.getDevice(name)
    motor.setPosition(float('inf'))
    # TODO should the velocity be set to 1.0? 
    motor.setVelocity(0.0)
    motor_dict[name] = motor

# Display the welcome message
print("Start the drone...")

# Wait one second 
while robot.step(timestep) != -1:
    if robot.getTime() > 1.0:
        break

# Constants, from the example on Cybernotics' Github
k_vertical_thrust = 68.5        # with this thrust, the drone lifts
k_vertical_offset = 0.6         # Vertical offset where the robot actually targets to stabilize itself
k_vertical_p = 3.0              # P constant for the vertical PID
k_roll_p = 50.0                 # P constant for the roll PID
k_pitch_p = 30.0                # P constant for the pitch PID

# Variables
target_altitude = 1.0           # Can be changed as desired

# Main loop:
# - perform simulation steps until Webots is stopping the controller
while robot.step(timestep) != -1:
    roll = devices_dict['inertial unit'].getRollPitchYaw()[0] + math.pi / 2.0
    pitch = devices_dict["inertial unit"].getRollPitchYaw()[1]
    altitude = devices_dict["gps"].getValues()[1]
    # TODO it appears that this example is using the ENU coordinate system, and this 
    # should be confirming it.
    roll_acceleration = devices_dict["gyro"].getValues()[0]
    pitch_acceleration = devices_dict["gyro"].getValues()[1]

    # TODO add camera roll and pitch stabilization
    # Stabilize the Camera by actuating the camera motors according to the gyro feedback

    # Transform the keyboard input to disturbances on the stabilization algorithm
    roll_disturbance = 0.0
    pitch_disturbance = 0.0
    yaw_disturbance = 0.0
    key = keyboard.getKey()
    while key > 0:
        if key == Keyboard.UP:
            pitch_disturbance = 2.0
            # TODO should it be break here as it is in the C example?
            # break
        elif key == Keyboard.DOWN:
            pitch_disturbance = -2.0
        elif key == Keyboard.RIGHT:
            yaw_disturbance = 1.3
        elif key == Keyboard.LEFT:
            yaw_disturbance = -1.3
        elif key == Keyboard.SHIFT + Keyboard.RIGHT:
            roll_disturbance = -1.0
        elif key == Keyboard.SHIFT + Keyboard.LEFT:
            roll_disturbance = 1.0
        elif key == Keyboard.SHIFT + Keyboard.UP:
            target_altitude += 0.05
            print(f"Target altitude = {target_altitude}")
        elif key == Keyboard.SHIFT + Keyboard.DOWN:
            target_altitude -= 0.05
            print(f"Target altitude = {target_altitude}")

        key = keyboard.getKey()

    # Compute  the roll, pitch, yaw and vertical inputs
    roll_input = k_roll_p * CLAMP(roll, -1.0, 1.0) + roll_acceleration + roll_disturbance
    pitch_input = k_pitch_p * CLAMP(pitch, -1.0, 1.0) - pitch_acceleration + pitch_disturbance
    yaw_input = yaw_disturbance
    clamped_difference_altitude = CLAMP(target_altitude - altitude + k_vertical_offset, -1.0, 1.0)
    vertical_input = k_vertical_p * pow(clamped_difference_altitude, 3.0)

    # Actuate the motors taking into consideration all the computed inputs
    front_left_motor_input = k_vertical_thrust + vertical_input - roll_input - pitch_input + yaw_input
    front_right_motor_input = k_vertical_thrust + vertical_input + roll_input - pitch_input - yaw_input
    rear_left_motor_input = k_vertical_thrust + vertical_input - roll_input + pitch_input - yaw_input
    rear_right_motor_input = k_vertical_thrust + vertical_input + roll_input + pitch_input + yaw_input

    motor_dict["front left propeller"].setVelocity(front_left_motor_input)
    motor_dict["front right propeller"].setVelocity(-front_right_motor_input)
    motor_dict["rear left propeller"].setVelocity(-rear_left_motor_input)
    motor_dict["rear right propeller"].setVelocity(rear_right_motor_input)

    


# Enter here exit cleanup code.
