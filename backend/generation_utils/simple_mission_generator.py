import json
import pprint
from collections import defaultdict
from json_reader_writer import json_reader_writer

"""
Generate a mission including many, many robots
"""


pp = pprint.PrettyPrinter()

robot_types = ["moose", "bb8", "pr2"]
js_r_w = json_reader_writer()
data = js_r_w.read_json("default_templates/default_data.json")
data["missions"]["GigaMission(!)"] = {"tasks": []}

# print(data)

n_robots = 5
id_number = 0
for i in range(len(robot_types)):
    for j in range(n_robots):
        new_task = {
            "name": f"task for {robot_types[i]}{id_number}",
            "id": id_number,
            "robot": f"{robot_types[i]}{j}",
            "simpleactions": [
                {
                    "name": "go_forward",
                    "args": "7",
                    "id": 0
                }
            ]
        }
        # data["Giga Mission(!)"]["tasks"].append(new_task)
        data["missions"]["GigaMission(!)"]["tasks"].append(new_task)
        print(f"addRobot({robot_types[i]}, \"{robot_types[i]}{j}\", 3, 3);")
        id_number += 1
        

# pp.pprint(data)
js_r_w.write_json("gigaMissionTest.json", json.dumps(data, indent=4))
print("Finished")
# pp.pprint(json.dumps(data))
# print(json.dumps(data))



