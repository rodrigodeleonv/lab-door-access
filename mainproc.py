import logging

from evdev import InputDevice
import yaml

from door_access.loggerconf import logging_config
from door_access.rfid_reader import main_loop  # , main
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


def entrypoint() -> None:
    """Entrypoint for the program."""
    config = get_config()
    DEV_NAME = config["readers"][0]["name"]
    URL = config["global"]["url"]
    LOG_LEVEL = config["global"]["log_level"]

    logging_config(LOG_LEVEL)

    logger.info("Starting RDIFD reader")
    logger.info(f"Log level: {LOG_LEVEL}")
    logger.info(f"Server URL: {URL}")

    device = find_rfid_reader(DEV_NAME)
    reader = InputDevice(device.path)
    try:
        main_loop(reader, URL)
    except KeyboardInterrupt:
        logger.info("RFID service stopped")
    except Exception:
        logger.exception("An exception occurred and program will closed")
    finally:
        reader.close()


if __name__ == "__main__":
    entrypoint()
