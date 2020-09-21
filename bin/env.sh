#!/bin/bash

sudo apt-get install -y python3.7
sudo apt-get install -y python3-setuptools
sudo apt-get install -y python3.7-venv

sudo python3.7 -m ensurepip
sudo python3.7 -m pip install virtualenv

sudo python3.7 -m venv ./venv
sudo ./venv/bin/python3.7 -m pip install --upgrade pip

source ./venv/bin/activate
sudo ./venv/bin/python3.7 -m pip install -r ./misc/requirements.txt
deactivate