"""moose_controller simpleactions."""
from controller import Robot, Motor
import threading
import time
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

        self.wheel_motors = {}
        # get the devices
        for i in range(8):
            self.wheel_motors[self.wheel_names[i]] = self.robot.getDevice(
                self.wheel_device_names[i])

        self.add_all_simpleactions()

    def add_all_simpleactions(self):
        self.add_available_simpleaction("go_forward", self.go_forward)

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
        for i in range(8):
            self.wheel_motors[self.wheel_names[i]
                              ].setVelocity(self.max_wheel_speed)
        if duration != 0:
            print(f"{self.robot_name} for {duration} seconds")
            time.sleep(duration)
            for i in range(8):
                self.wheel_motors[self.wheel_names[i]].setVelocity(0.0)

    def pr2_main(self):
        step_count = 0
        for i in range(8):
            self.wheel_motors[self.wheel_names[i]].setPosition(float('inf'))
            self.wheel_motors[self.wheel_names[i]].setVelocity(0.0)

        while self.robot.step(self.timestep) != -1:
            step_count += 1
