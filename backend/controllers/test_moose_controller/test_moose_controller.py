"""test_moose_controller controller."""

# You may need to import some classes of the controller module. Ex:
#  from controller import Robot, Motor, DistanceSensor
from controller import Robot, Motor

# create the Robot instance.
robot = Robot()

# get the time step of the current world.
timestep = int(robot.getBasicTimeStep())

names = ["left motor 1",  "left motor 2",  "left motor 3",  "left motor 4", "right motor 1", "right motor 2", "right motor 3", "right motor 4"]
motors = []

# enable all the devices
for name in names:
    motors.append(robot.getDevice(name))
    # motors[-1].enable(timestep)
    motors[-1].setPosition(float('inf'))


# Start all the motors
for motor in motors:
    motor.setVelocity(2.0)



# You should insert a getDevice-like function in order to get the
# instance of a device of the robot. Something like:
#  motor = robot.getDevice('motorname')
#  ds = robot.getDevice('dsname')
#  ds.enable(timestep)

# Main loop:
# - perform simulation steps until Webots is stopping the controller
while robot.step(timestep) != -1:
    # Read the sensors:
    # Enter here functions to read sensor data, like:
    #  val = ds.getValue()

    # Process sensor data here.

    # Enter here functions to send actuator commands, like:
    #  motor.setPosition(10.0)
    pass

# Enter here exit cleanup code.
