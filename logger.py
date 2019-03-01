# importing all required modules
import time
import glob
import logging
import logging.handlers

# Setting up LOGGER
LOG_FILENAME = '/home/pi/Projects/WaterLevelSensor/Log/wls_log'
wls_logger = logging.getLogger('wls_log')
wls_logger.setLevel(logging.DEBUG)
# Setting up Timed Rotating File Handler
handler = logging.handlers.TimedRotatingFileHandler(\
	LOG_FILENAME, when="midnight", backupCount=1000)
wls_logger.addHandler(handler)
