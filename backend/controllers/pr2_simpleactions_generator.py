"""moose_controller simpleactions."""
from controller import Robot, Motor
import threading
import time
from math import pi
from simpleactions_superclass import SimpleactionsSuperclass
from message_subscriber import MessageSubscriber


class Pr2SimpleactionsGenerator(SimpleactionsSuperclass):
    def __init__(self, name):
        super().__init__(name, "pr2")
        # create the Robot instance.

        # Define variables for this type of robot
        # maximum velocity for the wheels [rad / s]
        self.max_wheel_speed = 3.0
        # distance between 2 caster wheels (the four wheels are located in square) [m]
        self.wheels_distance = 0.4492
        # distance between 2 sub wheels of a caster wheel [m]
        self.sub_wheels_distance = 0.098
        self.wheel_radius = 0.08             # wheel radius

        # list of device names
        self.wheel_names = ["FLL_WHEEL", "FLR_WHEEL", "FRL_WHEEL",
                            "FRR_WHEEL", "BLL_WHEEL", "BLR_WHEEL", "BRL_WHEEL", "BRR_WHEEL"]
        self.wheel_device_names = ["fl_caster_l_wheel_joint", "fl_caster_r_wheel_joint",
                                   "fr_caster_l_wheel_joint", "fr_caster_r_wheel_joint", "bl_caster_l_wheel_joint", "bl_caster_r_wheel_joint", "br_caster_l_wheel_joint", "br_caster_r_wheel_joint"]

        self.rotation_names = ["FL_ROTATION",
                               "FR_ROTATION", "BL_ROTATION", "BR_ROTATION"]
        self.rotation_device_names = [
            "fl_caster_rotation_joint", "fr_caster_rotation_joint", "bl_caster_rotation_joint", "br_caster_rotation_joint"]

        self.rotation_motors = {}
        self.n_rotation_motors = 4
        # Get all the rotation devices and initiate the motors
        for i in range(self.n_rotation_motors):
            rotation_name = self.rotation_names[i]
            self.rotation_motors[rotation_name] = self.robot.getDevice(
                self.rotation_device_names[i])
            # self.rotation_motors[rotation_name]

        self.wheel_motors = {}
        self.n_wheel_motors = 8
        # Get the wheel devices and initiate the motors
        for i in range(self.n_wheel_motors):
            wheel_name = self.wheel_names[i]
            self.wheel_motors[wheel_name] = self.robot.getDevice(
                self.wheel_device_names[i])
            self.wheel_motors[wheel_name].setPosition(float('inf'))
            self.wheel_motors[wheel_name].setVelocity(0.0)

        self.add_all_simpleactions()

    def add_all_simpleactions(self):
        self.add_available_simpleaction("go_forward", self.go_forward)
        self.add_available_simpleaction("go_backward", self.go_backward)
        self.add_available_simpleaction("turn_right", self.turn_right)
        self.add_available_simpleaction("turn_left", self.turn_left)

    def initiate_threads(self):
        main = threading.Thread(target=self.pr2_main)
        # communication = threading.Thread(target=self.receive_routing_message)
        # location_communication = threading.Thread(target=self.receive_location)
        communication = threading.Thread(
            target=self.simpleactions_subscriber.subscription)
        main.start()
        communication.start()
        # communication.start()

    def go_forward(self, duration):
        self.set_wheel_speed(self.max_wheel_speed)
        if duration != 0:
            print(f"{self.robot_name} for {duration} seconds")
            time.sleep(duration)
            self.set_wheel_speed(0.0)

    def turn_right(self, duration):
        self.rotate(1, duration)

    def turn_left(self, duration):
        self.rotate(-1, duration)

    def rotate(self, angle, duration):
        # pi variables used to calculate the rotations
        PI = pi
        M_PI_2 = pi / 2
        M_PI_4 = pi / 4

        self.set_rotation_wheel_angles(
            3.0 * M_PI_4, M_PI_4, -3.0 * M_PI_4, -M_PI_4)

        if angle < 0:
            self.set_wheel_speed(self.max_wheel_speed)
        else:
            self.set_wheel_speed(-self.max_wheel_speed)
        if duration != 0:
            time.sleep(duration)
            self.set_rotation_wheel_angles(0.0, 0.0, 0.0, 0.0)
            self.set_wheel_speed(0.0)

    def set_rotation_wheel_angles(self, front_left, front_right, back_left, back_right):

        self.rotation_motors[self.rotation_names[0]].setPosition(front_left)
        self.rotation_motors[self.rotation_names[1]].setPosition(front_right)
        self.rotation_motors[self.rotation_names[2]].setPosition(back_left)
        self.rotation_motors[self.rotation_names[3]].setPosition(back_right)

    def enable_passive_wheels(self, enable):
        torques = [0.0 for _ in range(self.n_wheel_motors)]

        if enable:
            for i in range(self.n_wheel_motors):
                torques[i] = self.robot.getAvailableTorque(
                    self.wheel_motors[i])
                self.wheel_motors[i].setAvailableTorque(0.0)
        else:
            for i in range(self.n_wheel_motors):
                self.wheel_motors[i].setAvailableTorque(torques[i])

    def set_wheel_speed(self, speed):
        for i in range(self.n_wheel_motors):
            self.wheel_motors[self.wheel_names[i]
                              ].setVelocity(speed)

    def go_backward(self, duration):
        self.set_wheel_speed(-self.max_wheel_speed)
        if duration != 0:
            print(f"{self.robot_name} for {duration} seconds")
            time.sleep(duration)
            self.set_wheel_speed(0.0)

    def pr2_main(self):
        step_count = 0
        while self.robot.step(self.timestep) != -1:
            step_count += 1
