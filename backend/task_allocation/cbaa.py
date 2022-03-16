import json
import time
import requests

class CBAA:
    def __init__(self, robot_name, available_simpleactions, Nu):
        self.robot_name = robot_name
        self.available_simpleactions = available_simpleactions

        self.new_available_tasks = []
        self.task_work_list = []
        self.Nt = 0
        self.Nu = Nu

        self.x_vector = []
        self.y_vector = []
        self.winning_bid_list = []
        self.others_winning_bid_list = {}
        self.n_other_bids = 0
        self.winning_robots = []

    def select_task(self):
        """
        Basically, the robot creates a list including its highest bid it can make on a task.
        This is mostly used to utilize the algorithms "iterations through T steps" which calls this function for
        each step t.
        """
        # Algorithm 1
        # CBAA Phase 1 for agent i at iteration t

        # Display the available tasks for this agent
        # print(f"Available tasks for {self.robot_name}:")
        # for key, val in self.available_simpleactions.items():
        #     print(f"{key} : {val}")

        # Agent i's task list. Xij = 1 if agent i has been assigned to to task j, 0 otherwise
        self.x_vector = [0 for _ in range(self.Nt)]
        # winning bids ist
        # Yij is an up-to-date as possible estimate of the highest bid made for each task this far
        self.y_vector = [0 for _ in range(self.Nt)]
        if sum(self.x_vector) == 0:
            valid_tasks = self.indicator_function()
            print(f"Valid tasks for {self.robot_name}: {valid_tasks}")

            # Check if there were any valid tasks to choose from
            if any([x == 1 for x in valid_tasks]):
                # Loop through the y vector, and create a list only including the valid tasks from the valid task
                # list. Then select the maximum argument
                # task_J = max([y_vector[i] if valid_tasks[i] == 1 else 0 for i in range(len(y_vector))])
                task_j, task_j_index = self.get_max_value_and_index_of_valid_task_bid(valid_tasks)

                self.x_vector[task_j_index] = 1
                self.y_vector[task_j_index] = task_j

                # Second implementation:
                # Fill the y_vector with the cost of all the task, where y_vector[i] is the cost of executing task
                # with id i
                for task_id in range(self.Nt):
                    if valid_tasks[task_id] == 1:
                        self.y_vector[task_id] = self.cost_function(task_id)
                    else:
                        print(f"{self.robot_name} skipping task id {task_id}, values={self.task_work_list[task_id]}")

        print(f"After the first iteration of 'selected_tasks', we have the following values")
        print(f"{self.robot_name} x_vector: {self.x_vector}, y_vector={self.y_vector}")
        self.winning_bid_list = self.y_vector


    def get_winning_bids(self):
        # Important so send a copy of the list, and not a pointer to the list itself
        return self.winning_bid_list.copy()

    def receive_other_winning_bids(self, other_robot_name, other_bids):
        self.others_winning_bid_list[other_robot_name] = other_bids
        self.n_other_bids += 1


    def update_task(self):
        """
        The robots make use of a consensus strategy to converge on the list of winning bids and use that list to
        determine the winner. They compare each of the other robots' bids to their own, and updates their winning
        bids list accordingly. By this convention, each individual robot will reach a consensus on the winning robots.
        """
        print(f"Robot {self.robot_name} updating task")
        # consensus = [0 for _ in range(self.Nt)]
        consensus_bids = self.y_vector.copy()
        self.winning_robots = [self.robot_name for _ in range(self.Nt)]
        for other_robot_name, other_bid_list in self.others_winning_bid_list.items():
            # print(f"other_robot_name = {other_robot_name}, other bid list = {other_bid_list}")
            for task_id in range(self.Nt):
                nbr_bid = other_bid_list[task_id]
                if nbr_bid > self.y_vector[task_id]:
                    consensus_bids[task_id] = nbr_bid
                    # print(f"{self.name} got outbid on task id {task_id} by robot {other_robot_name}.\n"
                    #       f"Robots bid = {self.y_vector[task_id]}. Nbr bid = {nbr_bid}")
                    self.y_vector[task_id] = nbr_bid
                    self.winning_robots[task_id] = other_robot_name
                elif nbr_bid == self.y_vector[task_id]:
                    # print(f"Same bid on task id {task_id} by {self.name} and {other_robot_name}. "
                    #       f"Both bid {nbr_bid}. winning_robots[task_id] = {self.winning_robots[task_id]}")
                    # If they bid the same, compare the robot names to determine which one gets the bid.
                    # Note: don't compare other_robot_name to this robot name, as the bids for this current robot
                    # is highly dynamic and might have changed in the iterations in this function
                    # TODO compare them in some other fashion to determine the winner
                    if other_robot_name > self.winning_robots[task_id]:
                        # print(f"{other_robot_name} wins over {self.winning_robots[task_id}")
                        consensus_bids[task_id] = nbr_bid
                        self.y_vector[task_id] = nbr_bid
                        self.winning_robots[task_id] = other_robot_name

        for i in range(len(self.winning_robots)):
            # This robot loses its assignment if it has been outbid by another robot
            if self.winning_robots[i] != self.robot_name:
                self.x_vector[i] = 0

        print(f"{self.robot_name} with the current y_vector list: {self.y_vector}")
        print(f"{self.robot_name} with the current winning robots: {self.winning_robots}")
        # return consensus_bids

    def get_max_value_and_index_of_valid_task_bid(self, valid_tasks):
        """
        Find maximum score and its task index based on the current winning bids.
        This should only be relevant if the robot is to bid on only a single task, and is
        used to calculate its "best" task
        """
        max_value = 0
        index = 0
        # print(f"Initial max_value = {max_value}, index = {index}")
        for i in range(self.Nt):
            # if valid_tasks[i] == 1 and y_vector[i] > max_value:
            if valid_tasks[i] == 1 and self.cost_function(i) > self.y_vector[i] \
                    and self.cost_function(i) > max_value:
                max_value = self.cost_function(i)
                index = i
        return max_value, index

    def indicator_function(self):
        """
        Generates a list of the valid tasks for the robot. Checks if the task is possible for the robot
        to execute in general, then checks if the robot can bid a better bid than the current consensus bid on
        the task. (This last part is only relevant if there are several iterations of bids on the same tasks.

        Value for task j is 1:
            if it's a valid task, and
            0 otherwise
        """
        valid_tasks_h = []
        for j in range(self.Nt):
            # First, check if the current robot is able to perform the given task
            if not all([x in self.available_simpleactions.keys() for x in self.task_work_list[j]]):
                print(f"{self.robot_name} is not able to perform all the simpleactions in {self.task_work_list[j]}")
                valid_tasks_h.append(0)
                continue
            if self.cost_function(j) > self.y_vector[j]:
                valid_tasks_h.append(1)
            else:
                valid_tasks_h.append(0)
        return valid_tasks_h

    def cost_function(self, j):
        """
        Calculate the sum of the costs of all the simpleactions in a task.
        """
        total_cost = 0
        for simpleaction_name in self.task_work_list[j]:
            # Use an try/except here, however this should be already checked before this function is called, and
            # it should hopefully never have to throw this error.
            try:
                total_cost += self.available_simpleactions[simpleaction_name]
            except KeyError:
                print(f"Key error, no key named {simpleaction_name}")
        return total_cost
        # return self.available_tasks[j].cost

    def __str__(self):
        return f"{self.robot_name}, winning bid list = {self.winning_bid_list}\nOther Winning Bid List: {self.others_winning_bid_list}"

    def add_task_list(self, new_available_tasks):
        self.new_available_tasks = new_available_tasks
        for task in new_available_tasks:
            print(f"{self.robot_name} adding {task}")
            # self.task_work_list.extend(task["simpleactions"])
            self.task_work_list.append(task["simpleactions"])

        # Also update the number of tasks
        self.Nt = len(self.task_work_list)

    def confirm_all_bids(self, robot_name):
        retries = 0
        while self.n_other_bids < self.Nu - 1 and retries < 10:
            print(f"{robot_name} received {self.n_other_bids}/{self.Nu - 1}")
            time.sleep(0.5)
            retries += 1
        print(f"{robot_name} FINISHED RECEIVING. Received {self.n_other_bids}/{self.Nu - 1}")

    def post_results(self):
        """
        Send the results of the winning bids to the server
        This is done over HTTP with a POST request
        """
        result = []
        for task_id in range(self.Nt):
            # task_name = self.task_work_list[task_id]
            task_name = self.new_available_tasks[task_id]["name"]
            winner = self.winning_robots[task_id]
            result.append({"name": task_name, "robot": winner})
            # result["name"] = task_name
            # result["robot"] = winner

        print(f"{self.robot_name} posting result {result}")
        requests.post("http://localhost:5000/cbaa_results", json=result)


