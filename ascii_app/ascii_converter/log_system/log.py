import logging
import sys


##
# Initializing log
# How to use log:
#
# logger.critical('This is a critical message.')
#
# logger.error('This is an error message.')
#
# logger.warning('This is a warning message.')
#
# logger.info('This is an informative message.')
#
# logger.debug('This is a low-level debug message.')
#
# @param path_to_file path to log file, default value is empty string ant it means print log in console
# @return None or instance of logger
def initialize_log(path_to_log_file=""):
    try:
        logger = logging.getLogger()
        formatter = logging.Formatter("[ %(asctime)s - %(levelname)s - %(filename)s:%(lineno)s - %(funcName)1s() ] %(message)s")
        if path_to_log_file:
            handler = logging.FileHandler(path_to_log_file)
        else:
            handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(logging.DEBUG)
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger
    except:
        return None


##
# implementation of @Log
class Log:
    log = initialize_log()
