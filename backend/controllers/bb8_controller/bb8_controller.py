# from bb8_simpleactions import *
# init(5002, "bb8")

import sys
import os

controller_path = os.path.join(os.getcwd(), os.pardir)
sys.path.insert(0, controller_path)

from bb8_controller_generator import Bb8ControllerGenerator
bb8_controller = Bb8ControllerGenerator("bb8")
bb8_controller.initiate_threads()