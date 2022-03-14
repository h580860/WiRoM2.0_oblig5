# Source: Consensus-Based Decentralized Auctions for Robust
# Task Allocation
import threading
import random


class Agent:
    def __init__(self, name, tasks, robot_index, Nu):
        self.name = name
        self.tasks = tasks
        self.robot_index = robot_index
        self.Nt = len(tasks)
        self.Nu = Nu

        self.x_vector = []
        self.y_vector = []
        self.winning_bid_list = []
        self.others_winning_bid_list = {}

    def select_task(self):
        """
        Basically, the robot creates a list including its highest bid it can make on a task
        """
        # Algorithm 1
        # CBAA Phase 1 for agent i at iteration t

        # Display the available tasks for this agent
        print(f"Available tasks for {self.name}:")
        for x in self.tasks:
            print(x)

        # Agent i's task list. Xij = 1 if agent i has been assigned to to task j, 0 otherwise
        self.x_vector = [0 for _ in range(self.Nt)]
        # winning bids ist
        # Yij is an up-to-date as possible estimate of the highest bid made for each task this far
        self.y_vector = [0 for _ in range(self.Nt)]
        # indicator_function = \
        #     lambda cost_function, y_winning_bids_list : \
        #         [1 if cost_function(self.robot_index, j) > y_vector[j] else 0 for j in range(self.Nt)]
        if sum(self.x_vector) == 0:
            # valid_tasks = indicator_function(self.cost, y_vector)
            valid_tasks = self.indicator_function_self(self.cost_function, self.y_vector)
            print(f"Valid tasks for {self.name}: {valid_tasks}")
            if valid_tasks:
                # Loop through the y vector, and create a list only including the valid tasks from the valid task
                # list. Then select the maximum argument
                # task_J = max([y_vector[i] if valid_tasks[i] == 1 else 0 for i in range(len(y_vector))])
                task_j, task_j_index = self.get_max_value_and_index_of_valid_task_bid(self.y_vector, valid_tasks)
                print(f"task_j: {task_j} at index={task_j_index}")
                # Update the
                self.x_vector[task_j_index] = 1
                self.y_vector[task_j_index] = task_j

        print(f"After the first iteration of 'selected_tasks', we have the following values")
        print(f"x_vector: {self.x_vector}, y_vector={self.y_vector}")
        self.winning_bid_list = self.y_vector

    def get_winning_bids(self):
        return self.winning_bid_list

    def receive_other_winning_bids(self, other_robot_name, other_bids):
        self.others_winning_bid_list[other_robot_name] = other_bids

    def update_task(self):
        """
        Agents make use of a consensus strategy to converge on the list of winning bids and use that list to
        determine the winner.
        """
        print(f"Robot {self.name} updating task")
        # consensus = [0 for _ in range(self.Nt)]
        consensus_bids = self.y_vector.copy()
        winning_robots = [self.name for _ in range(self.Nt)]
        for other_robot_name, other_bid_list in self.others_winning_bid_list.items():
            for task_id in range(self.Nt):
                nbr_bid = other_bid_list[task_id]
                if nbr_bid > self.y_vector[task_id]:
                    consensus_bids[task_id] = nbr_bid
                    print(f"{self.name} got outbid on task id {task_id}.\n"
                          f"Robots bid = {self.x_vector[task_id]}. Nbr bid = {nbr_bid}")
                    self.y_vector[task_id] = nbr_bid
                    winning_robots[task_id] = other_robot_name
                elif nbr_bid == self.y_vector[task_id]:
                    print(f"Same bid on task id {task_id} by {self.name} and {other_robot_name}. "
                          f"Both bid {nbr_bid}")

        for i in range(len(winning_robots)):
            # This robot loses its assignment if it has been outbid by another robot
            if winning_robots[i] != self.name:
                self.x_vector[i] = 0

        return consensus_bids

    def get_max_value_and_index_of_valid_task_bid(self, y_vector, valid_tasks):
        max_value = self.cost_function(self.robot_index, 0)
        index = 0
        # print(f"Initial max_value = {max_value}, index = {index}")
        for i in range(index + 1, len(y_vector)):
            # if valid_tasks[i] == 1 and y_vector[i] > max_value:
            if valid_tasks[i] == 1 and self.cost_function(self.robot_index, i) > y_vector[i] \
                    and self.cost_function(self.robot_index, i) > max_value:
                max_value = self.cost_function(self.robot_index, i)
                index = i
        return max_value, index

    def indicator_function_self(self, cost_function, y):
        # Note: When run the first time, it will return a list of ones, because the winning bid list y_vector will
        # be initiated as a zero vector/list
        # TODO for it to be a valid task, the robot needs to be able to execute the task, i.e., the robot needs
        #  to be able to perform that simpleaction
        valid_tasks_h = []
        for j in range(self.Nt):
            if cost_function(self.robot_index, j) > y[j]:
                valid_tasks_h.append(1)
            else:
                valid_tasks_h.append(0)
        return valid_tasks_h

    def cost_function(self, robot_index, j):
        return self.tasks[j].cost

    def __str__(self):
        return f"{self.name}, winning bid list = {self.winning_bid_list}\nOther Winning Bid List: {self.others_winning_bid_list}"


class Task:
    def __init__(self, task_name, cost):
        self.task_name = task_name
        self.cost = cost

    def __str__(self):
        return f"{self.task_name}, cost={self.cost}"


def create_test_tasks(robotname):
    pass


if __name__ == '__main__':
    # robot_names = ["Robot1", "Robot2", "Robot3"]
    # test_tasks1 = create_test_tasks("Robot1")
    # test_tasks2 = create_test_tasks("Robot2")
    # test_tasks3 = create_test_tasks("Robot3")
    tasks0 = [Task("go_forward", 0.9), Task("turn_right", 0.5), Task("go_backwards", 0.7)]
    tasks1 = [Task("go_forward", 0.6), Task("turn_right", 0.8), Task("go_backwards", 0.7)]
    tasks2 = [Task("go_forward", 0.3), Task("turn_right", 0.3), Task("go_backwards", 0.4)]
    tasks3 = [Task("go_forward", 0.6), Task("turn_right", 0.95), Task("go_backwards", 0.85)]

    n_robots = 4
    robot0 = Agent("robot0", tasks0, 0, n_robots)
    robot1 = Agent("robot1", tasks1, 1, n_robots)
    robot2 = Agent("robot2", tasks2, 2, n_robots)
    robot3 = Agent("robot3", tasks3, 3, n_robots)
    all_robots = [robot0, robot1, robot2, robot3]

    # Phase 1
    for r in all_robots:
        r.select_task()
        print("-" * 30)

    # Phase 2
    # Generate the adjacency matrix. For now, everyone is connected to everyone.
    # By convention, every node has a self connecting edge
    adjacency_matrix = [[1 for _ in range(n_robots)] for _ in range(n_robots)]
    for x in adjacency_matrix:
        print(x)

    # Every agent receives a list of winning bids for each of its neighbours
    # This solution is meant for a fleet of robots where not necessarily every robots are currently neighbours.
    # In my case, where everyone are neighbours by default, there is no use for an adjacency matrix. However, for the
    # sake of possibly extending its functionalities later, we include the adjacency matrix here.
    for robot_id in range(n_robots):
        current_robot = all_robots[robot_id]
        for other_robot_id in range(n_robots):
            if robot_id == other_robot_id:
                # The robot's connection with itself in the matrix, so skip this one
                continue
            if adjacency_matrix[robot_id][other_robot_id] == 1:
                # They are neighbors
                other_robot = all_robots[other_robot_id]
                other_robot_bids = other_robot.get_winning_bids()
                current_robot.receive_other_winning_bids(other_robot.name, other_robot_bids)
                # print(f"{current_robot.name} receiving bids from {other_robot.name}")

    for robot in all_robots:
        print("-" * 30)
        print(f"{robot}")
    print("-" * 30)

    consensuses = []
    for robot in all_robots:
        consensuses.append(robot.update_task())

    print(f"All consensuses")
    for x in consensuses:
        print(x)
