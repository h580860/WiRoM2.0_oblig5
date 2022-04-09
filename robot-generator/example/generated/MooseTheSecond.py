import sys
import os

controller_path = os.path.join(os.getcwd(), os.pardir)
sys.path.insert(0, controller_path)

from moose_simpleactions_generator import MooseSimpleactionsGenerator
moose_simpleactions = MooseSimpleactionsGenerator("MooseTheSecond")
moose_simpleactions.initiate_threads()