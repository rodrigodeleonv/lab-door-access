import evdev
import pytest

from door_access import find_reader


def test_find_rfid_reader():
    devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
    assert find_reader.find_rfid_reader(devices[0].name) == devices[0]


def test_find_rfid_reade_not_found():
    with pytest.raises(find_reader.DeviceInputNotFound):
        find_reader.find_rfid_reader("Some device")
