#!/bin/bash

service dbus restart
service bluetooth restart
python3 ./main.py