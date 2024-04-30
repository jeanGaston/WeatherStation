#!/bin/bash

# Install Python3 and pip
sudo apt update
sudo apt install -y python3 python3-pip python3-flask python3-schedule

# Install required Python modules
pip3 install schedule
pip3 install bluepy

# Create env.py file
echo -n "Enter database file name (default: data.db): "
read db_file
db_file=${db_file:-data.db}


echo -e "DB_FILE = '$db_file'" > Program/env.py

# Execute main.py
cd Program
python3 main.py
