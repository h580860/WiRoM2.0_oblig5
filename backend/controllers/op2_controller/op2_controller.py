#from op2_simpleactions import *
#init(0, "op2")
import os
import sys

controller_path = os.path.join(os.getcwd(), os.pardir)
sys.path.insert(0, controller_path)

from op2_controller_class import Op2ControllerClass

op2_controller = Op2ControllerClass("op2")
op2_controller.initiate_threads()
