import json


class json_reader_writer():
    def __init__(self):
        pass

    
    def read_json(self, filename):
        '''
        Reads a json file and returns a Python Dictionary
        '''
        with open(filename, 'r', encoding='utf-8') as read_file:
            file_content = json.loads(read_file.read())
        return file_content


    def write_json(self, filename, content):
        with open(filename, 'w', encoding='utf-8') as writer_file:
            writer_file.write(content)
        print("Finished writing to file")