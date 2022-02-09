from controller import Robot


class BB8Controller():
    def __init__(self):
        # create the Robot instance.
        self.robot = Robot()

        # get the time step of the current world.
        self.timestep = int(self.robot.getBasicTimeStep())

        self.body_yaw_motor = self.robot.getDevice('body yaw motor')
        self.body_yaw_motor.setPosition(float('inf'))
        self.body_yaw_motor.setVelocity(0.0)

        self.body_pitch_motor = self.robot.getDevice('body pitch motor')
        self.body_pitch_motor.setPosition(float('inf'))
        self.body_pitch_motor.setVelocity(0.0)

        self.head_yaw_motor = self.robot.getDevice('head yaw motor')
        self.head_yaw_motor.setPosition(float('inf'))
        self.head_yaw_motor.setVelocity(0.0)

        self.yaw_speed = 0.0
        self.pitch_speed = 0.0
        self.max_speed = 4.0
        self.attenuation = 0.9

    def run(self):
        while self.robot.step(self.timestep) != -1:
            self.pitch_speed += self.attenuation 
            self.pitch_speed = min(self.max_speed, max(-self.max_speed, self.attenuation * self.pitch_speed))
            self.yaw_speed = min(self.max_speed, max(-self.max_speed, self.attenuation * self.yaw_speed))

            self.body_yaw_motor.setVelocity(self.yaw_speed)
            self.head_yaw_motor.setVelocity(self.yaw_speed)
            self.body_pitch_motor.setVelocity(self.pitch_speed)


if __name__ == '__main__':
    bb8_controller = BB8Controller()
    bb8_controller.run()
