# Source: Consensus-Based Decentralized Auctions for Robust
# Task Allocation
import threading
import random


class Agent:
    def __init__(self, name, tasks, robot_index):
        self.name = name
        self.tasks = tasks
        self.robot_index = robot_index
        self.Nt = len(tasks)

    def select_task(self):
        # Algorithm 1
        # CBAA Phase 1 for agent i at iteration t

        # Display the available tasks for this agent
        print(f"Available tasks for {self.name}:")
        for x in self.tasks:
            print(x)

        # Agent i's task list. Xij = 1 of agent i has been assigned to to task j, 0 otherwise
        x_vector = [0 for _ in range(self.Nt)]
        # winning bids ist
        # Yij is an up-to-date as possible estimate of the highest bid made for each task this far
        y_vector = [0 for _ in range(self.Nt)]
        # indicator_function = \
        #     lambda cost_function, y_winning_bids_list : \
        #         [1 if cost_function(self.robot_index, j) > y_vector[j] else 0 for j in range(self.Nt)]
        if sum(x_vector) == 0:
            # valid_tasks = indicator_function(self.cost, y_vector)
            valid_tasks = self.indicator_function_self(self.cost_function, y_vector)
            print(f"Valid tasks for {self.name}: {valid_tasks}")
            if valid_tasks:
                # Loop through the y vector, and create a list only including the valid tasks from the valid task
                # list. Then select the maximum argument
                # task_J = max([y_vector[i] if valid_tasks[i] == 1 else 0 for i in range(len(y_vector))])
                task_j, task_j_index = self.get_max_value_and_index_of_valid_task_bid(y_vector, valid_tasks)
                print(f"task_j: {task_j} at index={task_j_index}")
                # Update the
                x_vector[task_j_index] = 1
                y_vector[task_j_index] = task_j

        print(f"After the first iteration of 'selected_tasks', we have the following values")
        print(f"x_vector: {x_vector}, y_vector={y_vector}")

    def get_max_value_and_index_of_valid_task_bid(self, y_vector, valid_tasks):
        max_value = y_vector[0]
        index = 0
        for i in range(index + 1, len(y_vector)):
            if valid_tasks[i] == 1 and y_vector[i] > max_value:
                max_value = y_vector[i]
                index = i
        return max_value, index


    def indicator_function_self(self, cost_function, y):
        # Note: When run the first time, it will return a list of ones, because the winning bid list y_vector will
        # be initiated as a zero vector/list
        valid_tasks_h = []
        for j in range(self.Nt):
            if cost_function(self.robot_index, j) > y[j]:
                valid_tasks_h.append(1)
            else:
                valid_tasks_h.append(0)
        return valid_tasks_h

    def cost_function(self, robot_index, j):
        return self.tasks[j].cost


class Task:
    def __init__(self, task_name, cost):
        self.task_name = task_name
        self.cost = cost

    def __str__(self):
        return f"{self.task_name}, cost={self.cost}"


def create_test_tasks(robotname):
    pass


if __name__ == '__main__':
    robot_names = ["Robot1", "Robot2", "Robot3"]
    # test_tasks1 = create_test_tasks("Robot1")
    # test_tasks2 = create_test_tasks("Robot2")
    # test_tasks3 = create_test_tasks("Robot3")
    tasks1 = [Task("go_forward", 0.9), Task("turn_right", 0.5), Task("go_backwards", 0.7)]
    tasks2 = [Task("go_forward", 0.8), Task("turn_right", 0.4), Task("go_backwards", 0.7)]

    robot1 = Agent("robot1", tasks1, 0)
    robot2 = Agent("robot1", tasks2, 0)

    robot1.select_task()
    print("-" * 30)
    robot2.select_task()
