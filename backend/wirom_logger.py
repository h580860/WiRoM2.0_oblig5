import logging
import os

class Wirom_logger():

    def __init__(self, log_name):
        cwd = os.getcwd()
        logging.basicConfig(format='%(asctime)s %(message)s', filename=os.path.join(cwd, "logs", log_name), encoding='utf-8', level=logging.DEBUG)
        logging.info("-" * 50)

    # function call names mirros the actual logging function calls
    def debug(self, msg):
        logging.debug(msg)


    def info(self, msg):
        logging.info(msg)

    def error(self, msg):
        logging.error(msg)
    
    def critical(self, msg):
        logging.critical(msg)
