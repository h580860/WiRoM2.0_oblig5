from .task_allocation_superclass import TaskAllocationSuperclass


class CentralicedTaskAllocation(TaskAllocationSuperclass):
    """
    In this class we can add more methods related to centralized allocation algorithms
    """

    def __init__(self, algorithm_name):
        super().__init__(algorithm_name)

    def display_name(self):
        print(f"Centralized Task allocation algorithm: {self.algorithm_name}")
