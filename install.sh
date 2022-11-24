#!/bin/bash

pip3 install websockets picamera

crontab -l | { cat; echo "@reboot sleep 30 && /usr/bin/python3 $(pwd)/main.py"; } | crontab -