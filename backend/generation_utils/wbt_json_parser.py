import json
from os import path, truncate
import pathlib
import pprint


class WbtJsonParser:
    """
    This class reads the .wbt files and processes them as json documents, allowing for an
    adapter between the .wbt files which Webots use and regular json.
    The idea is to simplify interaction with the world files, and make them easier to read/write to.
    """

    def __init__(self, filepath=None, is_test=False):
        # self.filepath = filepath
        if is_test:
            self.filepath = pathlib.Path.cwd().parent / 'worlds' / 'test_parse_world.wbt'
        elif not filepath:
            self.filepath = pathlib.Path.cwd().parent / 'worlds' / 'delivery-missionUpdated.wbt'
        else:
            self.filepath = filepath

        self.key_name_count = {}
        self.file_content = {}
        self.subsection_types = ['normal', 'node', 'list']
        self.output_filename = "test_world_output.wbt"

    def read_file(self):
        '''
        Reads the original file and parses it to a more easy to handle json format
        '''
        with open(self.filepath, 'r') as reader:
            self.raw_file_content = reader.read().split('\n')
            # print(self.raw_file_content)
            # print(type(self.raw_file_content))
            # print(reader.read())

        # for x in self.raw_file_content:
        #     print(x)
        # print(self.raw_file_content)

        # Now we need to parse the input from the file
        self.file_header_line = self.raw_file_content[0]
        line_pointer = 1

        file_content = {}
        # file_content["header_line"] = header_line

        pp = pprint.PrettyPrinter(indent=4)

        count = 0
        while line_pointer < len(self.raw_file_content) - 1:
            # For each iteration in the loop, we want to parse one section at the time

            # The node name (which will be a key in the json file) will always be the first 
            # string of a section
            section_name = self.raw_file_content[line_pointer].split()[0]
            if section_name in file_content.keys():
                self.key_name_count[section_name] += 1
                section_name += str(self.key_name_count[section_name])
            else:
                self.key_name_count[section_name] = 1

            section_beginning = line_pointer + 1
            # print(f'section beginning at {section_beginning}')
            # Find section end. It ends if the first character on a line is an '}'
            while self.raw_file_content[line_pointer][0] != '}':
                line_pointer += 1

            section_end = line_pointer
            # print(f'section end at {section_end}. Line: {self.raw_file_content[section_end]}')

            section = self.raw_file_content[section_beginning:section_end]
            # print(f'SECTION {section}')

            count += 1
            # if count > 2:
            #     return
            # Recursively in case there are more subsections
            file_content[section_name] = self.handle_section(section_name, section, 1, "node")
            # print(f'filecontent: {json.dumps(file_content)}')
            # print("filecontent:")
            # pp.pprint(file_content)
            # print("Current File content")
            # print(file_content)

            line_pointer += 1
        # print("-" * 20 + " final file content " + "-" * 20)
        # # print(file_content)
        # for key, value in file_content.items():
        #     print(f'{key}: {value}')

        self.file_content = file_content

    def handle_section(self, name, section, indent_level, section_type):
        # print(f'Working with name: {name}, indlvl: {indent_level}, section: {section}')

        if section_type == "list" and len(section) == 1:
            # print("Returning list")
            return section

        # print(f'Working on section named {name}')
        if section_type == "list":
            current_section = []
        else:
            current_section = {}
        # current_section = {}
        ignore_sub_levels = False
        # for idx in range(len(section)):
        idx = 0
        while idx < len(section):
            # Remove the first whitespaces (indent level). One indent leven is 2 whitespaces
            # line = section[idx][indent_level * 2:].split()
            line = section[idx].strip().split()
            # print(f'working on line: {line}')

            if line[-1] == '{':
                # print("node")
                subsection_name = ' '.join(line[:-1])
                # print(f'subsection_name = {subsection_name}')
                subsection = []
                # while section[idx][indent_level * 2:].split() != '}':
                idx += 1
                # print(f'section[idx] out: {section[idx]}')
                # while not '}' in section[idx]:
                while section[idx][indent_level * 2] != '}':
                    # while section[idx].strip() != '}':
                    next_line = section[idx]
                    # print(f'section[idx] in: {section[idx]}. indlvl={indent_level}')
                    subsection.append(next_line)
                    idx += 1
                # print(f'Going in to subsection {subsection}')
                if section_type == "list":
                    current_section.append(
                        {subsection_name: self.handle_section(subsection_name, subsection, indent_level + 1, 'node')})
                else:
                    current_section[subsection_name] = self.handle_section(subsection_name, subsection,
                                                                           indent_level + 1, 'node')

                idx += 1
                continue

            if line[-1] == "[":
                # print("list")
                subsection_name = line[0]
                # print(f'subLIST name = {subsection_name}')
                subsection = []
                idx += 1
                while section[idx][indent_level * 2] != ']':
                    # while section[idx].strip() != ']':
                    # next_line = section[idx].strip()
                    next_line = section[idx]
                    # print(f'LISTsection[idx] in: {section[idx]}')
                    subsection.append(next_line)
                    idx += 1
                # print(f'Going in to subLISTsection {subsection}')
                if section_type == "list":
                    current_section.append(
                        {subsection_name: self.handle_section(subsection_name, subsection, indent_level + 1, "list")})
                else:
                    current_section[subsection_name] = self.handle_section(subsection_name, subsection,
                                                                           indent_level + 1, "list")
                # print(f'created list: {subsection}')
                # current_section[subsection_name] = subsection
                idx += 1
                continue

            key = line[0]
            values = []
            string_value = ""
            building_string_value = False
            # for i in range(1, len(line[1:])):
            i = 1
            while i <= len(line[1:]):
                # print(f'investigating {line[i]}')
                # if line[i] == "FALSE":
                #     values.append(False)
                #     break
                # elif line[i] == "TRUE":
                #     values.append(True)
                #     break
                # elif line[i][0] == "\"":
                if line[i][0] == "\"":
                    string_value += line[i]
                    # Check if there was only one word in the "" 
                    if line[i][-1] == "\"":
                        i += 1
                    else:
                        while line[i][-1] != "\"":
                            i += 1
                            string_value += " "
                            string_value += line[i]
                    # print('append normally 1')
                    values.append(string_value)
                    string_value = ""

                else:  # If none of the above, it's just a regular float value
                    # print(f"appending {line[i]}")
                    # print(f'append normally 2')
                    # values.append(float(line[i]))
                    values.append(line[i])
                i += 1

            # if section_type == "list":
            #     print("welp")
            # else:
            current_section[key] = " ".join(values)
            idx += 1
            # print(f'Updated current_section: {current_section}')
        # print(f"Done with section: {current_section}")
        # print(f'RETURNING. Current section: {current_section}')
        return current_section

    def write_node_to_file(self, node):
        '''
        Takes in a python dictionary, converts it to json and appends it at the end of the world file
        '''
        pass

    def read_position_of_node(self, node_name):
        '''
        Reads the "translation" field of a given node, and returns them as [x, y, z] positions
        '''
        pass

    def test_write_json_file(self):
        '''
        Write the content to a json file, just for manually testing to see if it works
        '''
        pass

    def write_file_to_json(self):
        with open('test.json', 'w', encoding='utf-8') as write_file:
            json.dump(self.file_content, write_file, ensure_ascii=False, indent=4)

    def get_file(self):
        return self.file_content

    def add_moose_to_world(self):
        pass

    def get_all_moose(self):
        """
        Returns a list of all the Moose nodes (objects) in the world file
        """
        if not self.file_content:
            print(f'Error, read the file first!')
            return []

        result = []
        for key, value in self.file_content.items():
            if key[:5] == "Moose":
                result.append(value)
        return result

    def transform_from_json_to_world(self, content, has_header=False):
        '''
        @param content: json object with the content to be written 
        '''
        new_file = []
        if has_header:
            new_file.append(self.file_header_line)

        digits = [str(x) for x in range(10)]
        # print(f'Content: {content}')
        # print(f'New file:\n{new_file}')
        for key, value in content.items():
            if key[-1] in digits:
                key = key[:-1]
            new_file.append(key + " {")
            self.transform_section(new_file, value, 1)
            new_file.append("}")

        return new_file

    def transform_section(self, new_file, object, indent_lvl):

        spaces = lambda x: x * 2 * " "

        # print(f"value={object}")
        if isinstance(object, str):
            new_file.append(object)
            return

        for key, value in object.items():
            if isinstance(value, str):
                new_file.append(spaces(indent_lvl) + key + " " + value)
            elif isinstance(value, dict):
                # print(f'isinstance dict: {value}')
                new_file.append(spaces(indent_lvl) + key + " {")
                self.transform_section(new_file, value, indent_lvl + 1)
                new_file.append(spaces(indent_lvl) + "}")
            elif isinstance(value, list):
                # print(f'isinstance list: {value}')
                new_file.append(spaces(indent_lvl) + key + " [")
                for x in value:
                    self.transform_section(new_file, x, indent_lvl + 1)
                new_file.append(spaces(indent_lvl) + "]")

    def write_to_world_file(self, new_file, output_file):
        with open(output_file, "w", encoding='utf-8') as write_file:
            for i in range(len(new_file) - 1):
                write_file.write(new_file[i] + "\n")

            # Write the last line without appending a newline at the end
            write_file.write(new_file[-1])

    def append_to_world_file(self, node):
        #   new_part = self.transform_from_json_to_world(node)
        with open(self.filepath, "a", encoding='utf-8') as write_file:
            write_file.write("\n")
            for i in range(len(node) - 1):
                write_file.write(node[i] + "\n")

            # Write the last line without appending a newline at the end
            write_file.write(node[-1])

    def test_compare_infile_outfile(self):
        # Just for good measure, read the output file, and compare it to the first file we read
        with open(self.output_filename, 'r') as reader:
            output_file = reader.read().split('\n')

        # Compare the output file to the first read input file
        for i in range(len(output_file)):
            if not self.raw_file_content[i] == output_file[i]:
                print(
                    f'ERROR: raw_input_file not matching output file:\n{self.raw_file_content[i]} != {output_file[i]}')
                return False

        return True


if __name__ == "__main__":
    parser = WbtJsonParser(is_test=True)
    # parser = WbtJsonParser()
    # print(pathlib.Path.cwd().parent / 'backend' / 'worlds')

    parser.read_file()
    # parser.write_file_to_json()
    new_file = parser.transform_from_json_to_world(parser.file_content, has_header=True)
    parser.write_to_world_file(new_file, parser.output_filename)

    if parser.test_compare_infile_outfile():
        print("All good when comparing the input and output file!")
    else:
        print("Something went wrong when comparing the files")
