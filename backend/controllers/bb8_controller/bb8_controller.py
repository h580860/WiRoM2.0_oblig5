# from bb8_simpleactions import *
# init(5002, "bb8")

import sys
import os

controller_path = os.path.join(os.getcwd(), os.pardir)
sys.path.insert(0, controller_path)

from bb8_controller_class import Bb8ControllerClass
bb8_controller = Bb8ControllerClass("bb8")
bb8_controller.initiate_threads()