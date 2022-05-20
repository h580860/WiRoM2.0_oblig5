
import sys
import os
# Since Webots runs in a "sandbox environment", we need to modify the path to import the
# simpleactions class
controller_path = os.path.join(os.getcwd(), os.pardir)
sys.path.insert(0, controller_path)

from pr2_controller_class import Pr2ControllerClass
pr2_controller = Pr2ControllerClass("pr2")
pr2_controller.initiate_threads()
