import random
import pprint

from ..task_allocation.centralized_taskallocation import CentralicedTaskAllocation


class RandomAllocation(CentralicedTaskAllocation):
    def __init__(self, algorithm_name):
        super().__init__(algorithm_name)

    def random_allocation(self, tasks, robots):
        pp = pprint.PrettyPrinter()
        # pp.pprint(robots)
        for task in tasks:
            # Choose a random robot to allocate the task to. Check if it's a valid
            # assignment, and continue until it is valid
            robot_set = list(robots.keys())
            print(f"robot set = {robot_set}")
            while robot_set:
                assigned_robot = random.choice(robot_set)
                print(f"current assigned robot = {assigned_robot}")
                # Check if the chosen robot can perform the simpleaction
                # if all([simpleaction in robots[assigned_robot]["simpleactions"] for simpleaction in task["simpleactions"]]):
                # if any([simpleaction not in robots[assigned_robot]["simpleactions"] for simpleaction in task["simpleactions"]]):
                if self.valid_task(task, assigned_robot, robots):
                    task["robot"] = assigned_robot
                    print(
                        f"{assigned_robot} can perform each simpleaction in {task}")
                    break
                else:
                    print(
                        f"{assigned_robot} CANNOT perform each simpleaction in {task}")
                    robot_set.remove(assigned_robot)
        print(f"tasks")
        pp.pprint(tasks)
        return tasks


# # TODO this function needs to be automatically inserted into each generated file. At least
# # that would make it much easier to implement
# # def valid_task(task, robot_name, robots):
# #     return any([simpleaction["name"] not in robots[robot_name]["simpleactions"] for simpleaction in task["simpleactions"]])

# def valid_task(task, robot_name, robots):
#     """
#     Check if a task is valid for a given robot name
#     Checks every simpleaction in the task to see if the robot is capable of performing this simpleaction
#     """
#     robot_simpleactions = robots[robot_name]["simpleactions"]
#     robot_simpleactions_names = [x["name"] for x in robot_simpleactions]

#     for x in task["simpleactions"]:
#         task_name = x["name"]
#         if task_name not in robot_simpleactions_names:
#             print(f"{robot_name} CANNOT perform {task_name}")
#             return False
#         else:
#             print(f"{robot_name} can perform {task_name}")

#     return True
