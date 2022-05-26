class TaskAllocationSuperclass:
    def __init__(self, algorithm_name):
        self.algorithm_name = algorithm_name

    def valid_task(self, task, robot_name, robots):
        """
        Check if a task is valid for a given robot name
        Checks every simpleaction in the task to see if the robot is capable of performing this simpleaction

        Parameters
        ---------
        task: list
            The task to be checked, which consist of a list of simpleactions
        robot_name : str
            Name of the current robot, for which we are checking the validity of the task for
        robots : dict
            Dictionary with the robot names as keys and their data as values. One of these values
            is a list of the simpleactions
        """
        robot_simpleactions = robots[robot_name]["simpleactions"]
        robot_simpleactions_names = [x["name"] for x in robot_simpleactions]

        for x in task["simpleactions"]:
            task_name = x["name"]
            if task_name not in robot_simpleactions_names:
                print(f"{robot_name} CANNOT perform {task_name}")
                return False
            else:
                print(f"{robot_name} can perform {task_name}")

        return True
