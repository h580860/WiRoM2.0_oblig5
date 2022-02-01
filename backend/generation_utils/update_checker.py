import pathlib
import os
import shutil
import json
from backend.generation_utils.json_reader_writer import json_reader_writer
from backend.generation_utils.wbt_json_parser import WbtJsonParser


# TODO this should perhaps be renamed
class UpdateChecker:
    '''
    Class that checks if there has been added any new robots using the 
    Robotgenerator DSL
    '''

    def __init__(self):
        # print(f"current working directory using pathlib= {pathlib.Path.cwd()}")
        # print(f"current working directory using OS= {os.getcwd()}")
        self.json_reader_writer = json_reader_writer()

        self.update_file = pathlib.Path.cwd() / "generation_utils" / "added_robots.json"
        self.save_file_content = self.json_reader_writer.read_json(self.update_file)
        self.prev_added_robots = self.save_file_content["previouslyAddedRobots"]
        self.new_added_robots = self.save_file_content["newAddedRobots"]
        self.controller_base_path = pathlib.Path.cwd() / "controllers"
        self.current_portnumber = 5002
        self.map_reader = WbtJsonParser()
        self.configpath = pathlib.Path.cwd() / 'config.json'
        self.datapath = pathlib.Path.cwd().parent / 'web_interface' / 'src' / 'data.json'

        self.robot_types_capital_lookup = {
            "moose": "Moose",
            "mavic2pro": "Mavic2Pro"
        }


    # def read_template(self, robotType):
    #     template = self.json_reader_writer.read_json(
    #         pathlib.Path.cwd().parent / 'generation_utils' / f"{self.robot_type}_template.json")
    #     return template

    def add_robot_to_world(self, robot, robot_data, robot_type, world_template, controller_name):
        '''
        Reads the current map file, and adds the robot as a node
        Also calculates its new position, based on the other robot on the map
        Returns this new position, to be used later in the config and data file
        '''
        robot_type_capitalized = self.robot_types_capital_lookup[robot_type]
        new_robot_node = world_template[robot_type_capitalized]
        self.map_reader.read_file()

        all_robots = self.map_reader.get_all_of_robot_type(robot_type_capitalized)
        all_translations = []

        # The lowest transformation we are looking for will depend on which robot type we have
        # TODO Hardcoded. Not very dynamic
        # also TODO
        if robot_type == "moose":
            # The "lowest transformation" will be the one with the lowest z value
            lowest_transformation = [0, 0, float('inf')]
            translation_index = 2
        elif robot_type == "mavic2pro":
            translation_index = 0
            lowest_transformation = [float('inf'), 0, 0]
        else:
            translation_index = 0
            lowest_transformation = [0, 0, float('inf')]

        for x in all_robots:
            translation = self.get_translation(x)
            if translation[translation_index] < lowest_transformation[translation_index]:
                lowest_transformation = translation
            all_translations.append(translation)

        new_transformation = lowest_transformation
        new_transformation[translation_index] = lowest_transformation[translation_index] - 5
        # Since we converted it to floats to do calculations, we need to convert them back to string
        new_transformation = " ".join([str(x) for x in new_transformation])
        new_positions = new_transformation

        # Update the translation of the new node
        new_robot_node["translation"] = new_transformation

        new_robot_node["name"] = f"\"{robot}\""
        # Set the controller
        new_robot_node["controller"] = f"\"{controller_name}\""

        # Wrap the json object with with a capitalized key
        new_robot_node = {robot_type_capitalized: new_robot_node}
        new_worldfile_content = self.map_reader.transform_from_json_to_world(new_robot_node)
        self.map_reader.append_to_world_file(new_worldfile_content)

        print(f"Finished writing to the world file. New positions are: {new_positions}")
        return new_positions

    def get_translation(self, node):
        translation = [float(x) for x in node["translation"].split()]
        return translation

    def add_robot_to_config(self, robot, robot_data, robot_type, new_positions, config_template):
        # updated_config_object = {robot: config_template[robot_type]}
        updated_config_object = config_template
        print(f"updated_config_object:\n{updated_config_object}")
        # del config_template
        new_x = new_positions[0]
        new_y = new_positions[1]

        updated_config_object["location"] = {
            "x": new_x,
            "y": new_y
        }

        # Increment the port number we are currently at

        updated_config_object["port"] = str(self.current_portnumber)

        key_name = robot
        # Now append the created robot data to the "robots" section in config

        # Get the actual content from the config file, so we can modify it
        config_content = self.json_reader_writer.read_json(self.configpath)
        config_content["robots"][key_name] = updated_config_object
        self.json_reader_writer.write_json(self.configpath, json.dumps(config_content, indent=4))
        print(f"Finished writing to config")

    def add_robot_to_data(self, robot, robot_data, robot_type, data_template):
        updated_data_object = data_template
        updated_data_object["port"] = str(self.current_portnumber)

        key_name = robot

        # Get the actual content from the data file, so we can modify it
        data_content = self.json_reader_writer.read_json(self.datapath)
        data_content["robots"][key_name] = updated_data_object
        self.json_reader_writer.write_json(self.datapath, json.dumps(data_content, indent=4))
        print("Finished writing to data")

    def add_robot_controller(self, robot, controller_name):
        controller_dir = self.controller_base_path / controller_name
        os.mkdir(controller_dir)
        print(f"Created directory at {controller_dir}")

        new_simpleactions_filename = f"{robot}_simpleactions.py"
        # TODO the source path will have to be wherever the DSL generator generates code
        source_filepath = pathlib.Path.cwd() / f"{robot}.py"
        destination_filepath = controller_dir / f"{controller_name}.py"

        # Copy the generated controller to the new controller's directory
        shutil.copy(source_filepath, destination_filepath)

        # TODO update the routing key lookup table

    def update_added_robots_json(self, robot):
        self.prev_added_robots.append(robot)
        # When one of the robots are added, remove all of the same type from the queue
        # while robot in self.save_file_content
        while robot in self.new_added_robots:
            self.new_added_robots.remove(robot)
        self.json_reader_writer.write_json(self.update_file, json.dumps(self.save_file_content))
        print(f"finished updating the save file")

    def count_robots_in_config(self, type, content):
        pass

    def initiate_full_robot_check(self):
        """
        Called by the server, and works as the "main" function for this class
        Check if there are any new robots added, and if there are, properly add them to the system
        Finally, save the system configuration with the newly added robots
        """

        if not self.new_added_robots:
            print(f"No new robots")
            return

        for robot in self.new_added_robots:

            # read the generated json file to fetch the data
            robot_data = self.json_reader_writer.read_json(f"{robot}.json")
            print(f"Robot data: {robot_data}")
            robot_type = robot_data["addRobot"]["type"]
            robot_template = self.json_reader_writer.read_json(
                pathlib.Path.cwd() / f"{robot_type}_template.json")

            robot_controller_name = f"{robot}_controller"
            world_template = robot_template["webots_world"]

            new_positions = self.add_robot_to_world(robot, robot_data, robot_type, world_template, robot_controller_name)
            self.current_portnumber += 1\

            config_template = robot_template["config"][robot_type]
            self.add_robot_to_config(robot, robot_data, robot_type, new_positions, config_template)

            data_template = robot_template["data"][robot_type]
            self.add_robot_to_data(robot, robot_data, robot_type, data_template)
            self.add_robot_controller(robot, robot_controller_name)

            self.update_added_robots_json(robot)


if __name__ == "__main__":
    update_checker = UpdateChecker()
    update_checker.initiate_full_robot_check()
