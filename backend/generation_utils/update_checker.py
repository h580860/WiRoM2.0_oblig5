import pathlib
import os
import shutil
import json
from backend.generation_utils.json_reader_writer import json_reader_writer
from backend.generation_utils.wbt_json_parser import WbtJsonParser
from backend.generation_utils.find_new_gen_robots import FindNewGenRobots


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

        # C:\Users\Gunnar\Documents\WiRoM2.0\dsl_robotgenerator\org.gunnarkleiven.robotgenerator.parent\org.gunnarkleiven.robotgenerator\sample\src
        # self.generated_files_filepath = pathlib.Path.cwd() / "dsl_robotgenerator" \
        #                                 / "org.gunnarkleiven.robotgenerator.parent" \
        #                                 / "org.gunnarkleiven.robotgenerator" / "sample" / "src-gen" / "robotgenerator"

        self.generated_files_filepath = pathlib.Path().parent / "robot-generator" / \
            "example" / "generated"
        self.update_file = pathlib.Path.cwd() / 'backend' / "generation_utils" / \
            "added_robots.json"
        self.save_file_content = self.json_reader_writer.read_json(
            self.update_file)
        self.prev_added_robots = self.save_file_content["previouslyAddedRobots"]
        self.new_added_robots = self.save_file_content["newAddedRobots"]
        self.controller_base_path = pathlib.Path.cwd() / "backend" / "controllers"
        self.current_portnumber = 5002
        self.map_filepath = pathlib.Path.cwd() / "backend" / "worlds" / \
            "delivery-missionUpdated.wbt"
        self.map_reader = WbtJsonParser(filepath=self.map_filepath)
        self.configpath = pathlib.Path.cwd() / 'backend' / 'config.json'
        self.datapath = pathlib.Path.cwd() / 'web_interface' / 'src' / 'data.json'

        self.robot_types_capital_lookup = {
            "moose": "Moose",
            "mavic2pro": "Mavic2Pro",
            "op2": "RobotisOp2",
            "bb8": "BB-8",
            "pr2": "Pr2"
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

        all_robots = []
        # All new robot translations are determined according to the one and only SPEEDSIGN, the most
        # default position if them all. I know that there is 1, so we can take the first item from the result list
        speed_sign = self.map_reader.get_all_of_robot_type("SpeedLimitSign")[0]

        default_translation = self.get_translation(speed_sign)

        for val in self.robot_types_capital_lookup.values():
            all_robots.extend(self.map_reader.get_all_of_robot_type(val))

        all_translations = []

        # The lowest transformation we are looking for will depend on which robot type we have
        # TODO Hardcoded. Not very dynamic
        # also TODO
        """
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
        
        """
        if robot_type == "mavic2pro":
            translation_index = 0
            lowest_transformation = [float('inf'), 0, 0]
        else:
            lowest_transformation = [0, 0, float('inf')]
            translation_index = 2

        # for x in all_robots:
        #     translation = self.get_translation(x)
        #     if translation[translation_index] < lowest_transformation[translation_index]:
        #         lowest_transformation = translation
        #     all_translations.append(translation)

        # new_transformation = lowest_transformation
        # new_transformation[translation_index] = lowest_transformation[translation_index] - 5

        new_transformation = default_translation
        # TODO this needs to be update if I change the coordination axis by updating to webots 2022
        z_value_offset = len(all_robots) * 2.5
        new_transformation[2] -= z_value_offset
        # Also increase the y-value, so the robot does not spawn in the ground
        new_transformation[1] += 0.3

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
        new_worldfile_content = self.map_reader.transform_from_json_to_world(
            new_robot_node)
        self.map_reader.append_to_world_file(new_worldfile_content)

        print(
            f"Finished writing to the world file. New positions are: {new_positions}")
        return new_positions

    def get_translation(self, node):
        translation = [float(x) for x in node["translation"].split()]
        return translation

    def add_robot_to_config(self, robot, robot_data, robot_type, new_positions, config_template):
        # updated_config_object = {robot: config_template[robot_type]}
        updated_config_object = config_template
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
        self.json_reader_writer.write_json(
            self.configpath, json.dumps(config_content, indent=4))
        print(f"Finished writing to config")

    def add_robot_to_data(self, robot, robot_data, robot_type, data_template):
        updated_data_object = data_template
        updated_data_object["port"] = str(self.current_portnumber)

        key_name = robot

        # Get the actual content from the data file, so we can modify it
        data_content = self.json_reader_writer.read_json(self.datapath)
        data_content["robots"][key_name] = updated_data_object
        self.json_reader_writer.write_json(
            self.datapath, json.dumps(data_content, indent=4))
        print("Finished writing to data")

    def add_robot_controller(self, robot, controller_name):
        controller_dir = self.controller_base_path / controller_name
        os.mkdir(controller_dir)
        print(f"Created directory at {controller_dir}")
        open(controller_dir / "__init__.py", 'a').close()

        # new_simpleactions_filename = f"{robot}_simpleactions.py"
        # simpleactions_source_filepath = self.generated_files_filepath / robot / new_simpleactions_filename
        # simpleactions_destination_filepath = controller_dir / new_simpleactions_filename

        # Copy the generated simpleactions implementations to the new controller's directory
        # shutil.copy(simpleactions_source_filepath, simpleactions_destination_filepath)
        # print(f"Copied simpleactions implementations for {robot}")

        new_controller_filename = f"{robot}_controller.py"
        controller_source_filepath = self.generated_files_filepath / new_controller_filename
        controller_destination_filepath = controller_dir / new_controller_filename
        shutil.copy(controller_source_filepath,
                    controller_destination_filepath)
        print(f"Copied controller implementation for {robot}")

        # key lookup table no longer in use
        # Update the routing key lookup table
        # routing_key_lookup_filepath = pathlib.Path.cwd() / "backend" / "routing_keys_lookup.json"
        # routing_key_lookup = self.json_reader_writer.read_json(routing_key_lookup_filepath)
        # routing_key_lookup[str(self.current_portnumber)] = f"{robot}_queue"
        # self.json_reader_writer.write_json(routing_key_lookup_filepath, json.dumps(routing_key_lookup, indent=4))

    def update_added_robots_json(self):
        # When one of the robots are added, remove all of the same type from the queue
        # while robot in self.save_file_content
        self.save_file_content["previouslyAddedRobots"] = self.prev_added_robots
        self.save_file_content["newAddedRobots"] = []
        self.json_reader_writer.write_json(
            self.update_file, json.dumps(self.save_file_content))
        print(f"finished updating the save file")

    def count_robots_in_config(self, type, content):
        pass

    def initiate_full_robot_check(self):
        """
        Called by the server, and works as the "main" function for this class
        Check if there are any new robots added, and if there are, properly add them to the system
        Finally, save the system configuration with the newly added robots
        """

        # Check if there has been generated any new files in the Eclipse run configuration workspace
        find_new_gen_robots = FindNewGenRobots(
            self.prev_added_robots, self.controller_base_path)
        self.new_added_robots = find_new_gen_robots.find_new_generated_robots()

        if not self.new_added_robots:
            print(f"No new robots")
            return

        for robot in self.new_added_robots:
            if robot in self.prev_added_robots:
                print(f"Skipping adding duplicate of {robot}")
                continue
            # read the generated json file to fetch the data
            robot_data = self.json_reader_writer.read_json(
                self.generated_files_filepath / robot / f"{robot}.json")
            # print(f"Robot data: {robot_data}")
            robot_type = robot_data["addRobot"]["type"]
            robot_template = self.json_reader_writer.read_json(
                pathlib.Path.cwd() / "backend" / "generation_utils" / f"{robot_type}_template.json")

            robot_controller_name = f"{robot}_controller"
            world_template = robot_template["webots_world"]

            new_positions = self.add_robot_to_world(robot, robot_data, robot_type, world_template,
                                                    robot_controller_name)
            self.current_portnumber += 1
            config_template = robot_template["config"][robot_type]
            self.add_robot_to_config(
                robot, robot_data, robot_type, new_positions, config_template)

            data_template = robot_template["data"][robot_type]
            self.add_robot_to_data(
                robot, robot_data, robot_type, data_template)
            self.add_robot_controller(robot, robot_controller_name)

            self.prev_added_robots.append(robot)
            # We remove this robot from the "queue", just in case it has been added multiple times

        self.update_added_robots_json()

    def update_everything_after_dsl_usage(self):
        with open((self.generated_files_filepath / "newRobots.txt"), 'r') as f:
            robots = set([x.strip() for x in f.readlines()])

        for robot in robots:
            if robot in self.prev_added_robots:
                print(f"Skipping adding duplicate of {robot}")
                continue
            # read the generated json file to fetch the data
            robot_data = self.json_reader_writer.read_json(
                self.generated_files_filepath / f"{robot}.json")
            # print(f"Robot data: {robot_data}")
            robot_type = robot_data["robotType"]
            robot_template = self.json_reader_writer.read_json(
                pathlib.Path.cwd() / "backend" / "generation_utils" / f"{robot_type}_template.json")

            robot_controller_name = f"{robot}_controller"
            world_template = robot_template["webots_world"]

            new_positions = self.add_robot_to_world(robot, robot_data, robot_type, world_template,
                                                    robot_controller_name)
            self.current_portnumber += 1
            config_template = robot_template["config"][robot_type]
            self.add_robot_to_config(
                robot, robot_data, robot_type, new_positions, config_template)

            data_template = robot_template["data"][robot_type]
            self.add_robot_to_data(
                robot, robot_data, robot_type, data_template)
            self.add_robot_controller(robot, robot_controller_name)

            self.prev_added_robots.append(robot)

        self.update_added_robots_json()


if __name__ == "__main__":
    update_checker = UpdateChecker()
    update_checker.initiate_full_robot_check()
