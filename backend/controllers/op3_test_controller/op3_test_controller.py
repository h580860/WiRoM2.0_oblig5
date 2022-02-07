"""op3_test_controller controller."""

# You may need to import some classes of the controller module. Ex:
#  from controller import Robot, Motor, DistanceSensor
from controller import Robot
import os
import sys
libraryPath = os.path.join(os.environ.get("WEBOTS_HOME"), 'projects', 'robots', 'robotis', 'darwin-op', 'libraries', 'python39')
libraryPath = libraryPath.replace('/', os.sep)
sys.path.append(libraryPath)
print(sys.path)
from managers import RobotisOp2MotionManager, RobotisOp2GaitManager


# Source: http://www.running-robot.net/en/notice-en/212.html

class Walk():
    def __init__(self):

        # create the Robot instance.
        self.robot = Robot()

        self.timestep = int(self.robot.getBasicTimeStep())
        self.head_led = self.robot.getLED('HeadLed')
        self.eye_led = self.robot.getLED('EyeLed')
        self.head_led.set(0xff0000)
        self.eye_led.set(0xa0a0ff)
        self.accelerometer = self.robot.Accelerometer('Accelerometer')
        self.accelerometer.enable(self.timestep)

        # Two variables which defines whether the robot falls or not
        self.fup = 0
        self.fdown = 0

        self.gyro = self.robot.getGyro('Gyro')
        self.gyro.enable(self.timestep)
        self.positionSensorNames = ['ShoulderR', 'ShoulderL', 'ArmUpperR', 'ArmUpperL',
                                    'ArmLowerR', 'ArmLowerL', 'PelvYR', 'PelvYL',
                                    'PelvR', 'PelvL', 'LegUpperR', 'LegUpperL',
                                    'LegLowerR', 'LegLowerL', 'AnkleR', 'AnkleL',
                                    'FootR', 'FootL', 'Neck', 'Head']

        self.positionSensors = []
        for i in range(len(self.positionSensorNames)):
            self.positionSensors.append(self.robot.getPositionSensor(self.positionSensorNames[i] + 'S'))
            self.positionSensors[i].enable(self.timestep)

        self.motion_manager = RobotisOp2MotionManager(self.robot)
        self.gait_manager = RobotisOp2GaitManager(self.robot, " Head ")

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
