# from backend.controllers.moose_controller.moose_simpleactions import *
import pathlib
import sys
import os
# from moose_simpleactions import *
# print(f"Sys path:\n{sys.path}")
# controller_path = pathlib.Path.cwd().parent.parent.parent
controller_path = os.getcwd()
controller_path = os.path.join(controller_path, os.pardir)
# TODO does this part only work on Windows?
# controller_path = controller_path.replace('\\', os.sep)
# print(os.getcwd())
sys.path.insert(0, controller_path)
# print(f"Sys path:\n{sys.path}")
# from backend.controllers.import_testing import ImportTesting
# from import_testing import ImportTesting
# print(f"Controller_path = {controller_path}")
# ImportTesting("From moose_controller")
# init(5002, "moose")


from moose_controller_generator import MooseControllerGenerator
moose_controller = MooseControllerGenerator("moose")
moose_controller.initiate_threads()