#!/bin/bash

install_dir="/opt/rfid-reader"

echo "Installing RFID Reader Service"

sudo mkdir -p $install_dir
sudo $(which python) -m venv $install_dir/.env

sudo /opt/rfid-reader/.env/bin/pip install -U pip setuptools wheel
sudo /opt/rfid-reader/.env/bin/pip install -i https://test.pypi.org/simple/ lab-door-access

# TODO: Modify URL for main branch
# sudo curl -o $install_dir/requirements.txt \
#     https://raw.githubusercontent.com/rodrigodeleonv/lab-door-access/dev/requirements-prod.txt
sudo curl -o $install_dir/mainproc.py \
    https://raw.githubusercontent.com/rodrigodeleonv/lab-door-access/dev/mainproc.py
# Download if not exists
# Check if the file already exists
if [ ! -f "$install_dir/config-reader.yml" ]; then
    # File doesn't exist, download it
    sudo curl -o $install_dir/config-reader.yml \
        https://raw.githubusercontent.com/rodrigodeleonv/lab-door-access/dev/config-reader-example.yml
else
    echo "File config-reader.yml already exists. Skipping download."
fi

# sudo curl -o /etc/supervisor/conf.d/usb-reader.conf \
#     https://raw.githubusercontent.com/rodrigodeleonv/lab-door-access/dev/usb-reader.conf

# sudo apt update
# sudo apt install supervisor -y

# sudo supervisorctl reread
# sudo supervisorctl update

# echo "Done. You need to configure $install_dir/config-reader.yml."
# echo -e "Then to start the service use: \e[1;32msudo supervisorctl restart rfid-usb-reader\e[0m"