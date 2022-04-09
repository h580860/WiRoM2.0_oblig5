import sys
import os

controller_path = os.path.join(os.getcwd(), os.pardir)
sys.path.insert(0, controller_path)

from mavic2pro_simpleactions_generator import Mavic2proSimpleactionsGenerator
mavic2pro_simpleactions = Mavic2proSimpleactionsGenerator("MavicTheSecond")
mavic2pro_simpleactions.initiate_threads()