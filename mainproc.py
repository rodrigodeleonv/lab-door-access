import logging
from time import sleep

from evdev import InputDevice
import yaml

from door_access.loggerconf import logging_config
from door_access.rfid_reader import main_loop
from door_access.find_reader import find_rfid_reader, DeviceInputNotFound

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


def get_reader(device_name: str, retry: int = 15) -> InputDevice:
    """Attempt to locate an RFID reader device by a known identifier in its name.

    It's a blocking operation until device is found.

    Args:
        device_name: the exact name of the device.
        retry: number of seconds to wait before retrying.

    Returns:
        RFID reader InputDevice.
    """
    while True:
        try:
            device = find_rfid_reader(device_name)
        except DeviceInputNotFound:
            logger.error(
                f"Device not found. Please connect device and wait for {retry} seconds"
            )
            sleep(retry)
        except KeyboardInterrupt:
            break
        else:
            break
    return InputDevice(device.path)


def entrypoint() -> None:
    """Entrypoint for the program."""
    config = get_config()
    DEV_NAME = config["readers"][0]["name"]
    URL = config["global"]["url"]
    LOG_LEVEL = config["global"]["log_level"]

    logging_config(LOG_LEVEL)

    logger.info("Starting RDIFD reader")
    logger.info(f"Log level: {LOG_LEVEL}")
    logger.info(f"RFID Device name: {DEV_NAME}")
    logger.info(f"Server URL: {URL}")

    while True:
        break_loop = True
        reader = get_reader(DEV_NAME, retry=10)
        try:
            main_loop(reader, URL)
        except OSError as e:
            if e.errno == 19:
                logger.exception("Device not found. Device was disconnected?")
                break_loop = False
                continue
        finally:
            reader.close()
            if break_loop:
                break


if __name__ == "__main__":
    try:
        entrypoint()
    except KeyboardInterrupt:
        logger.info("Program stopped")
    except Exception:
        logger.exception("An exception occurred and program will be closed")
