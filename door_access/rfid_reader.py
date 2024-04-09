import logging
from evdev import InputDevice, categorize, ecodes
from evdev.events import InputEvent  # , KeyEvent

logger = logging.getLogger(__name__)


def handle_key_press(data, rfid_tag: str):
    if 2 <= data.scancode <= 11:
        digit = str((data.scancode - 1) % 10)
        rfid_tag += digit
    elif data.scancode == 28:
        logger.info(f"RFID Tag ID: {rfid_tag}")
        rfid_tag = ""
    return rfid_tag


def main_loop(device_path: str):
    reader = InputDevice(device_path)
    logger.info(f"Listening for RFID scans on device: {reader.path}")
    rfid_tag = ""

    try:
        for event in reader.read_loop():
            # event: KeyEvent
            if event.type == ecodes.EV_KEY:
                data: InputEvent = categorize(event)
                if data.keystate == 1:
                    rfid_tag = handle_key_press(data, rfid_tag)
    except KeyboardInterrupt:
        logger.info("Exit from being reading")
    except Exception:
        logger.exception("An exception occurred and program will closed")
    finally:
        reader.close()
