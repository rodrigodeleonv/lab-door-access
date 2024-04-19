import logging

import yaml

from door_access.loggerconf import logging_config
from door_access.rfid_reader import main_loop
from door_access.find_reader import find_rfid_reader

logger = logging.getLogger(__name__)

CONFIG_PATHS = ["./config-reader.yml"]


def get_config() -> dict:
    for path in CONFIG_PATHS:
        try:
            with open(path, "r") as f:
                config = yaml.safe_load(f)
        except FileNotFoundError:
            if path == CONFIG_PATHS[-1]:
                raise ValueError("Config file not found")
            else:
                continue
        else:
            return config


def main() -> None:
    config = get_config()
    DEV_NAME = config["readers"][0]["name"]
    URL = config["global"]["url"]
    LOG_LEVEL = config["global"]["log_level"]

    logging_config(LOG_LEVEL)

    logger.info("Starting RDIFD reader")
    logger.info(f"Log level: {LOG_LEVEL}")
    logger.info(f"Server URL: {URL}")

    device = find_rfid_reader(DEV_NAME)
    main_loop(device.path, URL)


main()
