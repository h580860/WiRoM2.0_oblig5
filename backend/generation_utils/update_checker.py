import pathlib
import os
from json_reader_writer import json_reader_writer


# TODO this should perhaps be renamed
class UpdateChecker:
    '''
    Class that checks if there has been added any new robots using the 
    Robotgenerator DSL
    '''
    def __init__(self):
        self.json_reader_writer = json_reader_writer()
        self.update_file = pathlib.Path.cwd() / "added_robots.json"
        self.save_file_content = self.json_reader_writer.read_json(self.update_file)
        self.prev_added_robots = self.save_file_content["previouslyAddedRobots"]
        self.new_added_robots = self.save_file_content["newAddedRobots"]
        self.controller_base_path = pathlib.Path.cwd().parent / "controllers"


    def add_robot_to_world(self, robot):
        pass

    
    def add_robot_to_config(self, robot):
        pass

    
    def add_robot_to_data(self, robot):
        pass


    def add_robot_controller(self, robot):
        controller_dir = self.controller_base_path / f"{robot}_controller"
        os.mkdir(controller_dir)
        print(f"Created directory at {controller_dir}")

        new_simpleactions_filename = f"{robot}_simpleactions.py"
        source_filepath = controller_dir



    def update_added_robots_json(self, robot):
        pass        


    def initiate_full_robot_check(self):
        '''
        Called by the server, and works as the "main" function for this class
        Check if there are any new robots added, and if there are, properly add them to the system
        Finally, save the system configuration with the newly added robots
        '''

        if not self.new_added_robots:
            print(f"No new robots")
            return


        for robot in self.new_added_robots:
            self.add_robot_to_world(robot)
            self.add_robot_to_config(robot)
            self.add_robot_to_data(robot)
            self.add_robot_controller(robot)

            self.update_added_robots_json(robot)


if __name__ == "__main__":
    update_checker = UpdateChecker()
    update_checker.initiate_full_robot_check()


