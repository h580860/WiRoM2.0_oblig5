"""op3_test_controller controller."""

# You may need to import some classes of the controller module. Ex:
#  from controller import Robot, Motor, DistanceSensor
from controller import Robot
from controller import LED
import os
import sys
libraryPath = os.path.join(os.environ.get("WEBOTS_HOME"), 'projects', 'robots', 'robotis', 'darwin-op', 'libraries', 'python39')
libraryPath = libraryPath.replace('/', os.sep)
sys.path.append(libraryPath)
from managers import RobotisOp2MotionManager, RobotisOp2GaitManager


# Source: http://www.running-robot.net/en/notice-en/212.html

class Walk():
    def __init__(self):

        # create the Robot instance.
        self.robot = Robot()

        self.timestep = int(self.robot.getBasicTimeStep())
        # self.head_led = self.robot.getDevice('HeadLed')
        # self.eye_led = self.robot.getDevice('EyeLed')
        # self.head_led.set(0xff0000)
        # self.eye_led.set(0xa0a0ff)
        # self.accelerometer = self.robot.Accelerometer('Accelerometer')
        # self.accelerometer.enable(self.timestep)

        # Two variables which defines whether the robot falls or not
        self.fup = 0
        self.fdown = 0

        self.gyro = self.robot.getDevice('Gyro')
        self.gyro.enable(self.timestep)
        self.positionSensorNames = ['ShoulderR', 'ShoulderL', 'ArmUpperR', 'ArmUpperL',
                                    'ArmLowerR', 'ArmLowerL', 'PelvYR', 'PelvYL',
                                    'PelvR', 'PelvL', 'LegUpperR', 'LegUpperL',
                                    'LegLowerR', 'LegLowerL', 'AnkleR', 'AnkleL',
                                    'FootR', 'FootL', 'Neck', 'Head']

        self.positionSensors = []
        for i in range(len(self.positionSensorNames)):
            self.positionSensors.append(self.robot.getDevice(self.positionSensorNames[i] + 'S'))
            self.positionSensors[i].enable(self.timestep)

        self.keyboard = self.robot.getKeyboard()
        self.keyboard.enable(self.timestep)

        self.motion_manager = RobotisOp2MotionManager(self.robot)
        self.gait_manager = RobotisOp2GaitManager(self.robot, "")

        self.is_walking = False
    

    def run_with_keyboard(self):
        print("Press the spacebar to start/stop walking")
        print("Use the arrow keys to move the robot while walking")
        self.my_step()

        self.motion_manager.playPage(9)
        self.wait(200)

        
        while True:
            self.gait_manager.setXAmplitude(0.0)
            self.gait_manager.setYAmplitude(0.0)
            key = 0
            key = self.keyboard.getKey()
            if key == 32:
                if self.is_walking:
                    self.gait_manager.stop()
                    self.is_walking = False
                    self.wait(200)
                else:
                    self.gait_manager.start()
                    self.is_walking = True
                    self.wait(200)
            elif key == 315:    # up arrow, move forward
                self.gait_manager.setXAmplitude(1.0)
            elif key == 317:    # down arrow, move backward
                self.gait_manager.setXAmplitude(-1.0)
            elif key == 316:    # left arrow, turn left
                self.gait_manager.setAAmplitude(-0.5)
            elif key == 314:    # right arrow, turn right
                self.gait_manager.setAAmplitude(0.5)
            self.gait_manager.step(self.timestep)
            self.my_step()
        

    def my_step(self):
        ret = self.robot.step(self.timestep)
        if ret == -1:
            exit(0)

    def wait(self, ms):
        startTime = self.robot.getTime()
        s = ms / 1000
        while s + startTime >= self.robot.getTime():
            self.my_step()

    def run(self):
        self.my_step()  # Simulate a step to refresh the sensor reading

        self.motion_manager.playPage(9)
        self.wait(200)

        self.is_walking = False

        while True:
            self.gait_manager.start()  # Gait generator enters walking state
            self.gait_manager.setXAmplitude(1.0)  # Set robot forward
            self.gait_manager.step(self.timestep)  # Gait generator generates a step action
            self.my_step()


if __name__ == '__main__':
    walk = Walk()
    walk.run()
    # walk.run_with_keyboard()


"""This controller uses built-in motion manager modules to get the OP2 to walk.."""
"""
import os
import sys
from controller import Robot
from controller import LED

# Path operations to correctly locate the managers.
#if sys.version_info.major > 2:
    #sys.exit("RobotisOpManager library is available ony for Python 2.7")

libraryPath = os.path.join(os.environ.get("WEBOTS_HOME"), 'projects', 'robots', 'robotis', 'darwin-op', 'libraries', 'python37')
libraryPath = libraryPath.replace('/', os.sep)
sys.path.append(libraryPath)

from managers import RobotisOp2GaitManager, RobotisOp2MotionManager

# Names of position sensors needed to get the corresponding device and read the measurements.
positionSensorNames = ('ShoulderR', 'ShoulderL', 'ArmUpperR', 'ArmUpperL',
                       'ArmLowerR', 'ArmLowerL', 'PelvYR', 'PelvYL',
                       'PelvR', 'PelvL', 'LegUpperR', 'LegUpperL',
                       'LegLowerR', 'LegLowerL', 'AnkleR', 'AnkleL',
                       'FootR', 'FootL', 'Neck', 'Head')
# List of position sensor devices.
positionSensors = []

# Create the Robot instance.
robot = Robot()
basicTimeStep = int(robot.getBasicTimeStep())
# Initialize motion manager.
motionManager = RobotisOp2MotionManager(robot)
# Get the time step of the current world.
timestep = int(robot.getBasicTimeStep())

# Retrieve devices.
#headLed = robot.getDevice('HeadLed')
#eyeLed = robot.getDevice('EyeLed')
gyro = robot.getDevice('Gyro')

# Enable all the position sensors and populate the 'positionSensor' list.
for i in range(0, len(positionSensorNames)):
    positionSensors.append(robot.getDevice(positionSensorNames[i] + 'S'))
    positionSensors[i].enable(basicTimeStep)

# Initialize the LED devices.
#headLed.set(0xff0000)
#eyeLed.set(0xa0a0ff)
# Enable gyro device.
gyro.enable(basicTimeStep)

# Perform one simulation step to get sensors working properly.
robot.step(timestep)

# Page 1: stand up.
# Page 9: assume walking position.
motionManager.playPage(1, True)
motionManager.playPage(9, True)

# Initialize OP2 gait manager.
gaitManager = None
gaitManager = RobotisOp2GaitManager(robot, "")
gaitManager.start()
gaitManager.setXAmplitude(0.0)
gaitManager.setYAmplitude(0.0)
gaitManager.setBalanceEnable(True)
gaitAmplitude = 0.5
looptimes = 0

# Main loop: perform a simulation step until the simulation is over.
# At the beginning, start walking on the spot.
# After 45 timesteps, begin taking steps forward.
while robot.step(timestep) != -1:
    if looptimes == 45:
        gaitManager.setXAmplitude(gaitAmplitude)

    gaitManager.step(basicTimeStep)
    looptimes += 1

"""