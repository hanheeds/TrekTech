#!/bin/bash
# This script is used to initialize the development environment

python3 -m venv ./venv
if [ -d "venv/Scripts" ]
then
    source venv/Scripts/activate # windows
else
    source venv/bin/activate # mac/linux
fi
pip install -r requirements.txt
set -o allexport
source keys.env
set +o allexport
python3 myapp/manage.py migrate