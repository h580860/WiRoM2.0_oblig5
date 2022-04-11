
import sys
import os
# Since Webots runs in a "sandbox environment", we need to modify the path to import the
# simpleactions class
controller_path = os.path.join(os.getcwd(), os.pardir)
sys.path.insert(0, controller_path)

from pr2_simpleactions_generator import Pr2SimpleactionsGenerator
pr2_simpleactions = Pr2SimpleactionsGenerator("pr2")
pr2_simpleactions.initiate_threads()
