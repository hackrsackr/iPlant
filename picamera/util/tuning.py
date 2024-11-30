#!/usr/bin/python3
import time
import json
from picamera2 import Picamera2

with open('config.json', 'r') as f:
    cfg = json.load(f)

# config
timestamp = time.strftime("%b_%d_%Y_%H:%M:%S")
dir_name = f"{cfg['dir_path']}/{timestamp}"
filepath = f"{dir_name}/output.mp4"

tuning = Picamera2.load_tuning_file("imx477_noir.json")
print(tuning)

# picam2 = Picamera2(tuning=tuning)