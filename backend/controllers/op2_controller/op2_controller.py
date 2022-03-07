#from op2_simpleactions import *
#init(0, "op2")
import os
import sys

controller_path = os.path.join(os.getcwd(), os.pardir)
sys.path.insert(0, controller_path)

from op2_simpleactions_generator import Op2SimpleactionsGenerator

op2_simpleactions = Op2SimpleactionsGenerator("op2")
op2_simpleactions.initiate_threads()
