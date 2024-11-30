#!/usr/bin/python3
import time
import datetime
import os
import subprocess

from picamera2 import Picamera2

picam2 = Picamera2()
picam2.configure("viewfinder")
picam2.start()

# Give time for Aec and Awb to settle, before disabling them
time.sleep(1)
picam2.set_controls({"AeEnable": False, "AwbEnable": False, "FrameRate": 1.0})
# And wait for those settings to take effect
time.sleep(1)

number_of_photos: int = 5
# date = datetime.date.today()
# create directory for output
path = str(datetime.date.today())
isExist = os.path.exists(path)
if not isExist:
    os.makedirs(path)


start_time = time.time()
for i in range(1, number_of_photos):
    r = picam2.capture_request()
    r.save("main", f"{path}/image{i}.jpg")
    r.release()
    print(f"Captured image {i} of {number_of_photos} at {time.time() - start_time:.2f}s")


picam2.stop()