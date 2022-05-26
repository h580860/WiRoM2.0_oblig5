from .centralized_taskallocation import CentralicedTaskAllocation


class OriginalTaskAllocation(CentralicedTaskAllocation):
    def __init__(self, algorithm_name):
        super().__init__(algorithm_name)

    # automatic task allocation algorithm, auction-based solution
    # allocates tasks to robots based on highest bid
    def task_allocation(self, tasks, robots):
        # wirom_logger.info("task_allocation")
        bids = {}
        for task in tasks:
            bids[task["name"]] = {}
            for robot in robots:
                bids[task["name"]][robot] = {}
                bid = 1
                for simpleaction in task["simpleactions"]:
                    robot_simpleaction = list(filter(
                        lambda robot_simpleaction: robot_simpleaction["name"] == simpleaction["name"],
                        robots[robot]["simpleactions"]))
                    if robot_simpleaction != []:
                        robot_simpleaction[0].update(
                            {"args": simpleaction["args"]})
                        robot_simpleaction[0].update(
                            {"location": robots[robot]["location"]})

                        utility = self.calculate_utility(robot_simpleaction[0])
                        bid = bid * utility
                    else:
                        bid = 0
                bids[task["name"]][robot] = bid

        tasks = self.allocate_tasks_to_highest_bidder(tasks, bids)
        # print(f"Tasks after task_allocation = {task}")

        print("Tasks after task allocation")
        return tasks

    # Calculate the utility a robot has for a simpleaction (quality - cost)

    def calculate_utility(self, robot_simpleaction):
        utility = robot_simpleaction["quality"] - robot_simpleaction["cost"]
        # calculate cross dependencies: go to location only such simpleaction for now
        if robot_simpleaction["name"] == "go_to_location" and robot_simpleaction["args"] != "[]":
            robot_loc = robot_simpleaction["location"]
            targetlist = robot_simpleaction["args"].strip('][').split(', ')
            target = {"x": int(targetlist[0]), "y": int(targetlist[1])}
            distance = abs(robot_loc["x"] - target["x"] +
                           robot_loc["y"] - target["y"])
            # find distance from target location and normalize before adding to utility
            distNorm = (1 - distance / 100)
            if distNorm > 0.1:
                utility = utility * distNorm
            else:
                utility = utility * 0.1

        return utility

    # Sorting bids and allocates tasks to robots based on highest bid

    def allocate_tasks_to_highest_bidder(self, tasks, bids):
        print(f"")
        for bid in bids:
            highest_bidder = '--'
            for robot in bids[bid]:
                if highest_bidder == '--' and bids[bid][robot] > 0:
                    highest_bidder = robot
                elif highest_bidder != '--' and bids[bid][robot] > bids[bid][highest_bidder]:
                    highest_bidder = robot

            for task in tasks:
                if task["name"] == bid:
                    task["robot"] = highest_bidder

        return tasks
