import logging

from door_access.loggerconf import logging_config
from door_access.rfid_reader import main_loop
from door_access.find_reader import find_rfid_reader

logger = logging.getLogger(__name__)


#
# Hardcoded values
DEV_NAME = ""
URL = ""
LOG_LEVEL = logging.DEBUG
#

logging_config(LOG_LEVEL)

logger.info("Starting RDIFD reader")
logger.info(f"Log level: {LOG_LEVEL}")

device = find_rfid_reader(DEV_NAME)
main_loop(device.path, URL)
