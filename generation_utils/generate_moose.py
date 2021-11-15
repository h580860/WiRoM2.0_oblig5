from _typeshed import WriteableBuffer
from wbt_json_parser import wbt_json_parser


class generate_moose():
    def __init__(self):
        self.map_reader = wbt_json_parser()
        
        

    def update_world_file(self):
        self.map_reader.read_file()
        self.map_reader.add_moose()
        self.map_reader
            






if __name__ == "__main__":
    generate_moose = generate_moose()

