import importlib
# import backend.new_task_allocation_algorithms.test.func as f
# my_module = importlib.import_module(backend.new_task_allocation_algorithms.test)
# from backend.new_task_allocation_algorithms

my_module = importlib.import_module(
    "backend.new_task_allocation_algorithms.test")

# my_module.func()
method_to_call = getattr(my_module, 'func')
method_to_call()
