import json
import sys
import pathlib

# TODO is this the best fix?
sys.path.insert(0, pathlib.Path.cwd().parent.parent.__str__())
# print(sys.path)
from backend.generation_utils.wbt_json_parser import WbtJsonParser
from backend.generation_utils.json_reader_writer import json_reader_writer
# import backend.generation_utils.wbt_json_parser
# import backend.generation_utils.json_reader_writer
import shutil
import os


class GenerateRobot:
    def __init__(self, robot_type="moose"):
        self.robot_type = robot_type
        self.robot_type_capital_lookup = {
            "moose": "Moose",
            "mavic2pro": "Mavic2Pro"
        }
        # self.robot_type_capital = f"{self.robot_type[0].upper()}{self.robot_type[1:]}"
        self.robot_type_capital = self.robot_type_capital_lookup[self.robot_type]
        self.map_reader = WbtJsonParser()
        self.json_reader_writer = json_reader_writer()
        self.robot_template = self.read_template()
        self.configpath = pathlib.Path.cwd().parent / 'config.json'
        self.datapath = pathlib.Path.cwd().parent.parent / 'web_interface' / 'src' / 'data.json'
        self.new_positions = []
        self.config_content = self.json_reader_writer.read_json(self.configpath)
        self.robot_count = self.count_robot(self.config_content["robots"])
        self.new_robot_number = self.robot_count + 1
        self.new_port_number = self.find_next_port_number(self.config_content["robots"])
        self.new_robot_name = f"{self.robot_type}{self.new_robot_number}"
        self.new_robot_controller_name = f"{self.robot_type}_controller{self.new_robot_number}"
        # self.new_dir_filepath = pathlib.Path.cwd().parent / 'controllers' / f'{self.robot_type}_controller{self.new_robot_number}'
        self.new_dir_filepath = pathlib.Path.cwd().parent / 'controllers' / self.new_robot_controller_name
        self.next_port_number = self.find_next_port_number(self.config_content["robots"])
        self.routing_key_lookup_filepath = pathlib.Path.cwd().parent / 'routing_keys_lookup.json'
        self.save_file = pathlib.Path.cwd().parent / 'generation_utils' / 'configurations_savefile.txt'



    def read_template(self):
        template = self.json_reader_writer.read_json(
            pathlib.Path.cwd().parent / 'generation_utils' / f"{self.robot_type}_template.json")
        return template

    def add_robot_to_world(self):
        # new_robot_node = self.robot_template["webots_world"]["Moose"]
        new_robot_node = self.robot_template["webots_world"][self.robot_type_capital]

        self.map_reader.read_file()
        all_robots = self.map_reader.get_all_of_robot_type(self.robot_type_capital)
        all_translations = []

        # The lowest transformation we are looking for will depend on which robot type we have
        # TODO Hardcoded. Not very dynamic
        if self.robot_type == "moose":
            # The "lowest transformation" will be the one with the lowest z value
            lowest_transformation = [0, 0, float('inf')]
            translation_index = 2
        elif self.robot_type == "mavic2pro":
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
        self.new_positions = new_transformation
        # Since we converted it to floats to do calculations, we need to convert them back to string
        new_transformation = " ".join([str(x) for x in new_transformation])

        # Update the translation on the new node
        new_robot_node["translation"] = new_transformation
        # print(f'Updated moose node: {new_robot_node}')

        # new_robot_node["name"] = f"\"moose{self.new_moose_number}\""
        new_robot_node["name"] = f"\"{self.new_robot_name}\""
        # Set the controller
        # new_robot_node["controller"] = f"\"moose_controller{self.new_moose_number}\""
        new_robot_node["controller"] = f"\"{self.new_robot_controller_name}\""
        new_robot_node = {f"{self.robot_type_capital}": new_robot_node}

        new_file_content = self.map_reader.transform_from_json_to_world(new_robot_node)
        self.map_reader.append_to_world_file(new_file_content)

    def get_translation(self, node):
        translation = [float(x) for x in node["translation"].split()]
        return translation

    def add_robot_to_config(self):
        # config_content = self.json_reader_writer.read_json(self.configpath)
        # print(f'Config content: {config_content}')

        robot_config_from_template = self.robot_template["config"][self.robot_type]
        if not self.new_positions:
            print("Haven't fetched the positions from the world file yet. Setting them to default 0, 0")
            new_x, new_y = 0, 0
        else:
            new_x = self.new_positions[0]
            # TODO I am currently using the z position from the translation to add to the x and y position
            new_y = self.new_positions[2]

        # Set the new positions in the node fetched from the template
        robot_config_from_template["location"] = {
            "x": new_x,
            "y": new_y
        }
        # Set the port
        # self.new_port_number = self.find_next_port_number(self.config_content["robots"])
        robot_config_from_template["port"] = str(self.new_port_number)

        # The count of moose robots will determine the key name (which needs to be unique)

        # key_name = "moose" + str(self.moose_count + 1)
        key_name = self.new_robot_name

        # Now append the created moose data to the "robots" sections in config
        self.config_content["robots"][key_name] = robot_config_from_template
        # Print it to output file
        # self.json_reader_writer.write_json("test_config.json", json.dumps(config_content, indent=2))
        self.json_reader_writer.write_json(self.configpath, json.dumps(self.config_content, indent=2))

    def add_robot_to_data(self):
        data_content = self.json_reader_writer.read_json(self.datapath)

        robot_data_from_template = self.robot_template["data"][self.robot_type]

        # Add the port
        # self.new_port_number = self.find_next_port_number(data_content["robots"])
        print(f'New port number: {self.new_port_number}')
        robot_data_from_template["port"] = str(self.new_port_number)

        # The count of moose robots will determine the key name (which needs to be unique)
        # key_name = "moose" + str(self.moose_count + 1)
        key_name = self.new_robot_name

        data_content["robots"][key_name] = robot_data_from_template

        # Update the testmission
        new_mission = {
            "name": f"Test: move forward {self.new_robot_name}",
            "id": 0,
            "robot": f"{self.new_robot_name}",
            "simpleactions": [
                {
                    "name": "go_forward",
                    "args": "10",
                    "id": 0
                }
            ]
        }
        if self.robot_type == "mavic2pro":
            mavic_set_altitude = {
                "name": "set_altitude",
                "args": "1",
                "id": 0
            }
            new_mission["simpleactions"][0]["id"] = 1
            new_mission["simpleactions"].insert(0, mavic_set_altitude)

        data_content["missions"]["Testmission"]["tasks"].append(new_mission)

        # self.json_reader_writer.write_json("test_data.json", json.dumps(data_content, indent=4))
        self.json_reader_writer.write_json(self.datapath, json.dumps(data_content, indent=4))

    def find_next_port_number(self, content):
        '''
        Goes through the config file, and finds all the used port numbers.
        Returns the new port number, which is the highest number previously used + 1
        '''
        largest_port_number = 0
        for value in content.values():
            # print(f'key: {key}, val: {value}')
            port = int(value["port"])
            if port > largest_port_number:
                largest_port_number = port

        return largest_port_number + 1

    def count_robot(self, content):
        count = 0
        for key in content.keys():
            if key[:len(self.robot_type)] == self.robot_type:
                count += 1
        return count

    def add_robot_controller(self):
        print(f'Creating new dir at {self.new_dir_filepath}')
        os.mkdir(self.new_dir_filepath)

        new_simpleactions_filename = f'{self.robot_type}_simpleactions{self.new_robot_number}.py'
        source_filepath = pathlib.Path.cwd().parent / 'controllers' / f'{self.robot_type}_controller' / f'{self.robot_type}_simpleactions.py'

        destination_filepath = self.new_dir_filepath / new_simpleactions_filename
        shutil.copy(source_filepath, destination_filepath)

        with open(self.new_dir_filepath / f'{self.robot_type}_controller{self.new_robot_number}.py', 'w') as writer:
            # remove .py
            writer.write(f"from {new_simpleactions_filename[:-3]} import *\n")
            writer.write(f"init({self.next_port_number}, \"{self.new_robot_name}\")\n")

        # Update the routing key lookup table
        routing_keys = self.json_reader_writer.read_json(self.routing_key_lookup_filepath)
        routing_keys[self.next_port_number] = f'{self.new_robot_name}_queue'
        self.json_reader_writer.write_json(self.routing_key_lookup_filepath, json.dumps(routing_keys, indent=4))

        # Save the configurations
        with open(self.save_file, 'a') as file_appender:
            file_appender.write(f'{self.new_robot_controller_name}\n')

        return self.new_robot_name

    def reset_to_default(self):
        '''
        Reset the configurations to the default templates. This action deletes all the added configurations, using the
        default templates found in generation_utils/default_templates
        '''

        # Reset the world file
        # reset_map_reader = WbtJsonParser(filepath='default_templates/delivery-missionUpdatedTemplate.wbt')
        reset_world_source_filepath = pathlib.Path.cwd().parent / 'generation_utils' / 'default_templates' / 'delivery-missionUpdatedTemplate.wbt'
        reset_world_destination_filepath = pathlib.Path.cwd().parent / 'worlds' / 'delivery-missionUpdated.wbt'
        shutil.copy(reset_world_source_filepath, reset_world_destination_filepath)
        print("world reset finished")

        # Reset the config file
        reset_config_source_filepath = pathlib.Path.cwd().parent / 'generation_utils' / 'default_templates' / 'default_config.json'
        reset_config_destination_filepath = self.configpath
        shutil.copy(reset_config_source_filepath, reset_config_destination_filepath)
        print("config reset finished")

        # Reset the data file
        reset_data_source_filepath = pathlib.Path.cwd().parent / 'generation_utils' / 'default_templates' / 'default_data.json'
        reset_data_destination_filepath = self.datapath
        shutil.copy(reset_data_source_filepath, reset_data_destination_filepath)
        print("config reset finished")

        # Reset the routing_keys_lookup file
        reset_routing_source_filepath = pathlib.Path.cwd().parent / 'generation_utils' / 'default_templates' / 'default_routing_keys_lookup.json'
        reset_routing_destination_filepath = pathlib.Path.cwd().parent / 'routing_keys_lookup.json'
        shutil.copy(reset_routing_source_filepath, reset_routing_destination_filepath)
        print("routing_key_lookup reset finished")

        # Access the save file to see how many controllers have been created
        # TODO better exception handling
        if pathlib.Path(self.save_file).exists():
            with open(self.save_file, 'r') as reader:
                save_file_content = reader.readlines()
            # Delete the controllers
            for controller in save_file_content:
                current_controller_filepath = pathlib.Path.cwd().parent / 'controllers' / controller.strip()
                if current_controller_filepath.is_dir():
                    shutil.rmtree(current_controller_filepath)
                    print(f'Deleted directory: {current_controller_filepath}')
                else:
                    print(f"No controller in: {current_controller_filepath}")

            # Delete the configuration savefile
            os.remove(self.save_file)
        print(f'Finished reset')


if __name__ == '__main__':
    try:
        args = sys.argv[:3]
    except IndexError:
        raise SystemExit(f"Error, no argument provided. Either <generate> <robottype (moose or mavic2pro)>"
                         f" or <reset>, omitting \"<>\"")
    print(f"Arguments = {args}")
    if args[1] != "generate" and args[1] != "reset":
        print(f'Invalid argument: {args[1]}')
        sys.exit(0)

    if len(args) > 2 and args[2] not in ["moose", "mavic2pro"]:
        print(f'Invalid robot argument: {args[2]}')
        sys.exit(0)

    if args[1] == "generate":
        generate_moose = GenerateRobot(args[2])
        generate_moose.add_robot_to_world()
        generate_moose.add_robot_to_config()
        generate_moose.add_robot_to_data()
        generate_moose.add_robot_controller()
    else:
        generate_moose = GenerateRobot()
        generate_moose.reset_to_default()
