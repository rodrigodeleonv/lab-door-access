#!/bin/bash

install_dir="/opt/rfid-reader"

echo -e "\nInstalling RFID Reader Service"

sudo mkdir -p $install_dir
sudo $(which python) -m venv $install_dir/env

sudo /opt/rfid-reader/env/bin/pip install -U pip setuptools wheel
sudo /opt/rfid-reader/env/bin/pip install -U lab-door-access
# #
# # TODO: remove. For test pypi can install dependencies
# sudo /opt/rfid-reader/env/bin/pip install -i https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple lab-door-access
# #

sudo curl -o $install_dir/mainproc.py \
    https://raw.githubusercontent.com/rodrigodeleonv/lab-door-access/main/mainproc.py

# Avoid alter existing config file: check if the file already exists
if [ ! -f "$install_dir/config-reader.yml" ]; then
    # File doesn't exist, download it
    sudo curl -o $install_dir/config-reader.yml \
        https://raw.githubusercontent.com/rodrigodeleonv/lab-door-access/main/config-reader-example.yml
else
    echo "File config-reader.yml already exists. Skipping download."
fi

sudo apt update
sudo apt install supervisor -y

sudo curl -o /etc/supervisor/conf.d/usb-reader.conf \
    https://raw.githubusercontent.com/rodrigodeleonv/lab-door-access/main/usb-reader.conf

sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl restart rfid-usb-reader

echo "Done. You need to configure $install_dir/config-reader.yml before service can start."
echo -e "Then to start the service use: \e[1;32msudo supervisorctl restart rfid-usb-reader\e[0m"