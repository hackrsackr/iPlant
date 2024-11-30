#!/usr/bin/python3
import time
import json
import os
import smtplib

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart

from picamera2 import Picamera2

with open('config.json', 'r') as f:
    cfg = json.load(f)

# config
timestamp = time.strftime("%b_%d_%Y_%H:%M:%S")
dir_name = f"{cfg['dir_path']}/{timestamp}"
os.makedirs(dir_name)
filepath = f"{dir_name}/output.mp4"

tuning = Picamera2.load_tuning_file("imx477_noir.json")
picam2 = Picamera2(tuning=tuning)
config = picam2.create_preview_configuration()
picam2.configure(config)
picam2.start()

# Give time for Aec and Awb to settle, before disabling them
time.sleep(1)
picam2.set_controls({"AeEnable": False, "AwbEnable": False, "FrameRate": 1.0})
# And wait for those settings to take effect
time.sleep(1)


start_time = time.time()
# Take pictures
for i in range(0, cfg['number_of_photos']):
    # r = picam2.capture_request(wait=cfg['secs_between_photos'])
    r = picam2.capture_request()
    time.sleep(cfg['secs_between_photos'])
    r.save("main", f"{dir_name}/image{i}.jpg")
    r.release()
    print(f"Captured image {i} of {cfg['number_of_photos']} at {time.time() - start_time:.2f}s")

picam2.stop()

# convert jpgs to mp4
os.chdir(dir_name)
os.system("ffmpeg -framerate 1 -pattern_type glob -i '*.jpg' -c:v libx264 -r 30 -pix_fmt yuv420p output.mp4")

# Initializing video object
video_file = MIMEBase('application', "octet-stream")

# Importing video file
video_file.set_payload(open(filepath, "rb").read())
video_file.add_header('content-disposition', 'attachment; filename={}'.format(filepath))

# Encoding video for attaching to the email
encoders.encode_base64(video_file)

from_addr = cfg['from_addr']
to_addr = cfg['to_addr']
subject = f"{cfg['subject']}_{timestamp}"
content = timestamp

# creating EmailMessage object
msg = MIMEMultipart()

# Loading message information ---------------------------------------------
msg['From'] = from_addr
msg['To'] = to_addr
msg['Subject'] = subject
msg['content'] = content

msg.attach(video_file)

server = smtplib.SMTP('smtp.gmail.com', 587)
server.ehlo()
server.starttls()
server.login(from_addr, cfg['app_password'])
server.send_message(msg, from_addr=from_addr, to_addrs=[to_addr])