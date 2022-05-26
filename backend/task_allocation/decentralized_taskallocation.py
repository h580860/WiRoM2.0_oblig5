from .task_allocation_superclass import TaskAllocationSuperclass


class DecentralicedTaskAllocation(TaskAllocationSuperclass):
    """
    In this class we can add more methods related to centralized allocation algorithms
    """

    def __init__(self, algorithm_name):
        super().__init__(algorithm_name)
