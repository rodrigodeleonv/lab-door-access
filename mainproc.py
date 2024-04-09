import logging

from door_access.loggerconf import logging_config
from door_access.rfid_reader import main_loop
from door_access.find_reader import find_rfid_reader

logger = logging.getLogger(__name__)
logging_config()

# Hardcoded name
device = find_rfid_reader("Sycreader RFID Technology Co., Ltd SYC ID&IC USB Reader")
main_loop(device.path)
