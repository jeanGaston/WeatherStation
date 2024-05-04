#!/bin/bash

# Install Python3 and pip
sudo apt update
sudo apt install -y python3 python3-pip python3-flask python3-schedule python3-plotly python3-pandas

# Install required Python modules
pip3 install bluepy 

# Create env.py file
echo -n "Enter database file name (default: data.db): "
read db_file
db_file=${db_file:-data.db}
echo -e "DB_FILE = '$db_file'" > Program/env.py

echo -n "Enter database file name (default: data.db): "
read db_file
db_file=${db_file:-data.db}

echo -n "Enter smtp server address : "
read smtp
echo -e "SMTP = '$smtp'" > Program/env.py

echo -n "Enter smtp port (default 25) : "
read smtp_port
smtp_port=${smtp_portx:-25}
echo -e "SMTP_PORT = $smtp_port" > Program/env.py


echo -n "Enter sender email address, used as smtp id : "
read smtp_id
echo -e "SMTP_ID = '$smtp_id'" > Program/env.py

echo -n "Enter sender password, used as smtp password : "
read smtp_pwd
echo -e "SMTP_PWD = '$smtp_pwd'" > Program/env.py

echo -n "Enter recipient email address : "
read recipient
echo -e "RECIPIENT = '$recipient'" > Program/env.py


echo -n "Enter Humidity rate alert threshold without percent symbol (default 70): "
read hr_max
hr_max=${hr_max:-70}
echo -e " MAX_HR= $hr_max" > Program/env.py

echo -n "Enter temperature alert threshold withpercent °c symbole (default 30) : "
read temp_max
temp_max=${temp_max:-30}
echo -e " MAX_TEMP= $temp_max" > Program/env.py

echo -e " SENSORS= {"d6:c6:c7:39:a2:e8":"DEMO3", "d6:1c:bf:b7:76:62":"DEMO1", "d7:ef:13:27:15:29":"DEMO2"} " > Program/env.py


# Execute main.py
cd Program
python3 main.py
