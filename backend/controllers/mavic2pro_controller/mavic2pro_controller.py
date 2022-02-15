# from backend.controllers.mavic2pro_controller.mavic2pro_simpleactions import *
# from mavic2pro_simpleactions import *
# init(5001, "mavic2pro")
import sys
import os
# Since Webots runs in a "sandbox environment", we need to modify the path to import the
# simpleactions class
controller_path = os.path.join(os.getcwd(), os.pardir)
sys.path.insert(0, controller_path)

from mavic2pro_simpleactions.mavic2pro_simpleactions_generator import Mavic2proSimpleactiosGenerator
mavic2pro_simpleactions = Mavic2proSimpleactiosGenerator("mavic2pro")
mavic2pro_simpleactions.initiate_threads()
