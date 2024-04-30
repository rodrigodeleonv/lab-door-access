#!/bin/bash

install_dir="/opt/rfid-reader"

echo -e "\nUninstalling RFID Reader Service"

sudo rm -rf $install_dir
sudo rm /etc/supervisor/conf.d/usb-reader.conf

echo -e "\nUninstall complete"
echo "Supervisor is not removed. You can remove it manually with: sudo apt remove --purge supervisor"
