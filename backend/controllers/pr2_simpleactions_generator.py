"""moose_controller simpleactions."""
from controller import Robot, Motor, PositionSensor
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

        # Math variables
        self.PI = pi
        self.M_PI_2 = pi / 2
        self.M_PI_4 = pi / 4

        # list of device names
        self.wheel_names = ["FLL_WHEEL", "FLR_WHEEL", "FRL_WHEEL",
                            "FRR_WHEEL", "BLL_WHEEL", "BLR_WHEEL", "BRL_WHEEL", "BRR_WHEEL"]
        self.wheel_device_names = ["fl_caster_l_wheel_joint", "fl_caster_r_wheel_joint",
                                   "fr_caster_l_wheel_joint", "fr_caster_r_wheel_joint", "bl_caster_l_wheel_joint", "bl_caster_r_wheel_joint", "br_caster_l_wheel_joint", "br_caster_r_wheel_joint"]

        self.rotation_names = ["FL_ROTATION",
                               "FR_ROTATION", "BL_ROTATION", "BR_ROTATION"]
        self.rotation_device_names = [
            "fl_caster_rotation_joint", "fr_caster_rotation_joint", "bl_caster_rotation_joint", "br_caster_rotation_joint"]

        self.arm_motor_names = [
            "SHOULDER_ROLL", "SHOULDER_LIFT", "UPPER_ARM_ROLL", "ELBOW_LIFT", "WRIST_ROLL"]

        # These names originally starts with either an l or an r, depending on if it's the left or the right arm
        self.arm_motor_device_names = ["_shoulder_pan_joint", "_shoulder_lift_joint",
                                       "_upper_arm_roll_joint", "_elbow_flex_joint", "_wrist_roll_joint"]

        self.left_arm_motors = {}
        self.left_arm_sensors = {}
        self.right_arm_motors = {}
        self.n_arm_motor_names = len(self.arm_motor_names)
        # Initiate the arm motors
        for i in range(self.n_arm_motor_names):
            name = self.arm_motor_names[i]
            self.left_arm_motors[name] = self.robot.getDevice(
                "l" + self.arm_motor_device_names[i])
            self.right_arm_motors[name] = self.robot.getDevice(
                "r" + self.arm_motor_device_names[i])

        self.rotation_motors = {}
        self.n_rotation_motors = 4
        # Get all the rotation devices and initiate the motors
        for i in range(self.n_rotation_motors):
            rotation_name = self.rotation_names[i]
            self.rotation_motors[rotation_name] = self.robot.getDevice(
                self.rotation_device_names[i])
            # self.rotation_motors[rotation_name]
            # TODO set the rotation motors position to float(inf)?

        self.wheel_motors = {}
        self.n_wheel_motors = 8
        self.wheel_position_sensors = {}
        # Get the wheel devices and initiate the motors
        for i in range(self.n_wheel_motors):
            wheel_name = self.wheel_names[i]
            self.wheel_motors[wheel_name] = self.robot.getDevice(
                self.wheel_device_names[i])
            self.wheel_motors[wheel_name].setPosition(float('inf'))
            self.wheel_motors[wheel_name].setVelocity(0.0)
            # self.wheel_position_sensors[wheel_name] = self.robot.getPositionSensor()
            self.wheel_position_sensors[wheel_name] = self.wheel_motors[wheel_name].getPositionSensor(
            )

            # Enable the sensors as well
            self.wheel_position_sensors[wheel_name].enable(self.timestep)

        # Initiate the torso motor
        self.torso_motor = self.robot.getDevice("torso_lift_joint")
        self.torso_motor.setPosition(float('inf'))

        # Get the forearm motors and initiate them
        self.left_forearm_motor = self.robot.getDevice("l_forearm_roll_joint")
        self.right_forearm_motor = self.robot.getDevice("r_forearm_roll_joint")

        # Arm positions
        self.initial_arm_position = (0.0, 1.35, 0.0, -2.2, 0.0)
        self.extended_arm_positions = (0.0, 0.5, 0.0, -0.5, 0.0)
        self.left_open_grab_arm_positions = (0.25, 0.5, -1.0, -0.5, 0.0)
        self.right_open_grab_arm_positions = (-0.25, 0.5, -1.0, -0.5, 0.0)
        self.left_closed_grab_arm_positions = (0.0, 0.5, -1.0, -1.0, 0.0)
        self.right_closed_grab_arm_positions = (0.0, 0.5, -1.0, -1.0, 0.0)

        self.add_all_simpleactions()

    def add_all_simpleactions(self):
        self.add_available_simpleaction("go_forward", self.go_forward)
        self.add_available_simpleaction("go_backward", self.go_backward)
        self.add_available_simpleaction("turn_right", self.turn_right)
        self.add_available_simpleaction("turn_left", self.turn_left)
        self.add_available_simpleaction("rotate_angle", self.rotate_angle)
        self.add_available_simpleaction("extend_arms", self.extend_arms)
        self.add_available_simpleaction("retract_arms", self.retract_arms)
        self.add_available_simpleaction("grab_box", self.grab_box)
        self.add_available_simpleaction("release_box", self.release_box)

    def initiate_threads(self):
        main = threading.Thread(target=self.pr2_main)
        # communication = threading.Thread(target=self.receive_routing_message)
        # location_communication = threading.Thread(target=self.receive_location)
        communication = threading.Thread(
            target=self.simpleactions_subscriber.subscription)
        main.start()
        communication.start()
        # communication.start()

    def set_initial_position(self):
        # self.set_left_arm_position(0.0, 1.35, 0.0, -2.2, 0.0)
        # self.set_right_arm_position(0.0, 1.35, 0.0, -2.2, 0.0)

        self.set_torso_height(0.3)
        # self.extend_arms()
        
        

    def set_left_arm_position(self, shoulder_roll, shoulder_lift, upper_arm_roll, elbow_lift, wrist_roll):
        self.left_arm_motors[self.arm_motor_names[0]
                             ].setPosition(shoulder_roll)
        self.left_arm_motors[self.arm_motor_names[1]
                             ].setPosition(shoulder_lift)
        self.left_arm_motors[self.arm_motor_names[2]
                             ].setPosition(upper_arm_roll)
        self.left_arm_motors[self.arm_motor_names[3]].setPosition(elbow_lift)
        self.left_arm_motors[self.arm_motor_names[4]].setPosition(wrist_roll)

    def set_right_arm_position(self, shoulder_roll, shoulder_lift, upper_arm_roll, elbow_lift, wrist_roll):
        self.right_arm_motors[self.arm_motor_names[0]
                              ].setPosition(shoulder_roll)
        self.right_arm_motors[self.arm_motor_names[1]
                              ].setPosition(shoulder_lift)
        self.right_arm_motors[self.arm_motor_names[2]
                              ].setPosition(upper_arm_roll)
        self.right_arm_motors[self.arm_motor_names[3]].setPosition(elbow_lift)
        self.right_arm_motors[self.arm_motor_names[4]].setPosition(wrist_roll)

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

        self.set_rotation_wheels_angles(
            3.0 * self.M_PI_4, self.M_PI_4, -3.0 * self.M_PI_4, -self.M_PI_4)

        if angle < 0:
            self.set_wheel_speed(self.max_wheel_speed)
        else:
            self.set_wheel_speed(-self.max_wheel_speed)
        if duration != 0:
            time.sleep(duration)
            self.set_rotation_wheels_angles(0.0, 0.0, 0.0, 0.0)
            self.set_wheel_speed(0.0)

    def set_rotation_wheels_angles(self, front_left, front_right, back_left, back_right):

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

    def extend_arms(self):
        # using * to unpack the tuple argument into separate variables
        self.set_left_arm_position(*self.extended_arm_positions)
        self.set_right_arm_position(*self.extended_arm_positions)

    def retract_arms(self):
        self.set_left_arm_position(*self.initial_arm_position)
        self.set_right_arm_position(*self.initial_arm_position)

    def grab_box(self):
        # Extend the arms
        # self.set_left_arm_position(*self.left_open_grab_arm_positions)
        # self.set_right_arm_position(*self.right_open_grab_arm_positions)
        # self.extend_arms()

        # Rotate the forearms
        # self.left_forearm_motor.setPosition(self.M_PI_2)
        # self.right_forearm_motor.setPosition(-self.M_PI_2)
        
       

        # Rotate the upper arm roll
        # Retrieve UPPER_ARM_ROLL
        name = self.arm_motor_names[2]
        self.left_arm_motors[name].setPosition(1.55)
        self.right_arm_motors[name].setPosition(-1.55)

        # Move slightly forward
        # self.go_forward(2)

        time.sleep(1)

        # Retrieve SHOULDER_ROLL 
        name = self.arm_motor_names[0]
        self.left_arm_motors[name].setPosition(-0.15)
        self.right_arm_motors[name].setPosition(0.15)

        # Grab the box
        # self.set_left_arm_position(*self.left_closed_grab_arm_positions)
        # self.set_right_arm_position(*self.right_closed_grab_arm_positions)


        # self.go_backward(5)

    def release_box(self):
          # Retrieve UPPER_ARM_ROLL
        name = self.arm_motor_names[2]
        self.left_arm_motors[name].setPosition(0)
        self.right_arm_motors[name].setPosition(0)

        time.sleep(1)

        # Retrieve SHOULDER_ROLL 
        name = self.arm_motor_names[0]
        self.left_arm_motors[name].setPosition(0)
        self.right_arm_motors[name].setPosition(0)

    def rotate_angle(self, angle):
        """
        Rotate the robot around itself given an angle in radian
        """
        angle = float(angle)
        # pi variables used to calculate the rotations

        self.set_rotation_wheels_angles(
            3.0 * self.M_PI_4, self.M_PI_4, -3.0 * self.M_PI_4, -self.M_PI_4)
        self.set_wheel_speed(
            (self.max_wheel_speed if angle > 0 else -self.max_wheel_speed))

        initial_wheel0_position = self.wheel_position_sensors[self.wheel_names[0]].getValue(
        )
        expected_travel_distance = abs(
            angle * 0.5 * self.wheels_distance + self.sub_wheels_distance)

        while True:
            wheel0_position = self.wheel_position_sensors[self.wheel_names[0]].getValue(
            )
            wheel0_travel_distance = abs(
                self.wheel_radius * (wheel0_position - initial_wheel0_position))

            if wheel0_travel_distance > expected_travel_distance:
                break

            # Reduce the speed before reaching the target
            if expected_travel_distance - wheel0_travel_distance < 0.025:
                self.set_wheel_speed(0.1 * self.max_wheel_speed)

            # self.step()

        # Reset the wheels
        self.set_rotation_wheels_angles(0.0, 0.0, 0.0, 0.0)
        self.set_wheel_speed(0.0)
        print("done rotating")

    def set_torso_height(self, height):
        self.torso_motor.setPosition(height)

    def step(self):
        """
        This particular robot type needs its own step method
        """
        return self.robot.step(self.timestep) != -1

    def pr2_main(self):
        step_count = 0

        self.set_initial_position()

        # while self.robot.step(self.timestep) != -1:
        while self.step():
            step_count += 1
            # print(f"{self.robot_name} step count = {step_count}")
