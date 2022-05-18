import random
from ..task_allocation.centralized_taskallocation import CentralicedTaskAllocation
class r2(CentralicedTaskAllocation):
	def __init__(self, algorithm_name):
		super().__init__(algorithm_name)

	def r2(self, tasks, robots):
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
	        return tasks
