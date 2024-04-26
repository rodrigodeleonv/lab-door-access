# lab-door-access

System service to control access to the Laboratory door.

```bash
sudo apt install supervisor -y
sudo $(which python) -m venv /opt/rfid-reader/env
sudo cp usb-reader.conf /etc/supervisor/conf.d/
sudo cp -r door_access mainproc.py /opt/rfid-reader
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl status
```

First, you need to identify the device. For example you have a USB RFID reader.
It's likely that your RFID reader is functioning as a keyboard emulation device (HID keyboard).

```bash
# Use one of the following commands
$ ls -lh /dev/input/by-id/
total 0
lrwxrwxrwx 1 root root 9 Mar 11 00:03 usb-Dell_Dell_USB_Keyboard-event-kbd -> ../event5
lrwxrwxrwx 1 root root 9 Mar 11 00:03 usb-Microsoft_Microsoft®_Nano_Transceiver_v1.0-event-if01 -> ../event2
lrwxrwxrwx 1 root root 9 Mar 11 00:03 usb-Microsoft_Microsoft®_Nano_Transceiver_v1.0-event-if02 -> ../event4
lrwxrwxrwx 1 root root 9 Mar 11 00:03 usb-Microsoft_Microsoft®_Nano_Transceiver_v1.0-event-kbd -> ../event0
lrwxrwxrwx 1 root root 9 Mar 11 00:03 usb-Microsoft_Microsoft®_Nano_Transceiver_v1.0-if01-event-mouse -> ../event1
lrwxrwxrwx 1 root root 9 Mar 11 00:03 usb-Microsoft_Microsoft®_Nano_Transceiver_v1.0-if01-mouse -> ../mouse0
lrwxrwxrwx 1 root root 9 Mar 11 00:03 usb-Microsoft_Microsoft®_Nano_Transceiver_v1.0-if02-event-kbd -> ../event3
lrwxrwxrwx 1 root root 9 Apr  8 13:26 usb-Sycreader_RFID_Technology_Co.__Ltd_SYC_ID_IC_USB_Reader_08FF20140315-event-kbd -> ../event8  # <-- This is the Device

# You need python evdev
$ python -m evdev.evtest
ID  Device               Name                                Phys                                Uniq
---------------------------------------------------------------------------------------------------------------------------------
0   /dev/input/event0    Microsoft Microsoft® Nano Transceiver v1.0 usb-0000:01:00.0-1.3/input0
1   /dev/input/event1    Microsoft Microsoft® Nano Transceiver v1.0 Mouse usb-0000:01:00.0-1.3/input1
2   /dev/input/event2    Microsoft Microsoft® Nano Transceiver v1.0 Consumer Control usb-0000:01:00.0-1.3/input1
3   /dev/input/event3    Microsoft Microsoft® Nano Transceiver v1.0 Consumer Control usb-0000:01:00.0-1.3/input2
4   /dev/input/event4    Microsoft Microsoft® Nano Transceiver v1.0 System Control usb-0000:01:00.0-1.3/input2
5   /dev/input/event5    Dell Dell USB Keyboard              usb-0000:01:00.0-1.4/input0
6   /dev/input/event6    vc4-hdmi-0                          vc4-hdmi-0/input0
7   /dev/input/event7    vc4-hdmi-1                          vc4-hdmi-1/input0
8   /dev/input/event8    Sycreader RFID Technology Co., Ltd SYC ID&IC USB Reader usb-0000:01:00.0-1.2/input0         08FF20140315  # <-- This is the Device
```
