# from bb8_simpleactions import *
# init(5002, "bb8")

import sys
import os

controller_path = os.path.join(os.getcwd(), os.pardir)
sys.path.insert(0, controller_path)

from bb8_simpleactions_generator import Bb8SimpleactionsGenerator
bb8_simpleactions = Bb8SimpleactionsGenerator("bb8")
bb8_simpleactions.initiate_threads()