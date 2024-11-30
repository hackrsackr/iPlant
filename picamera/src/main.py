#!/usr/bin/python3
import time
import json
import os
import smtplib

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart

from picamera2 import Picamera2, Preview

with open('config.json', 'r') as f:
    cfg = json.load(f)

# config
photos      = cfg['number_of_photos']
photo_delay = cfg['secs_between_photos']
app_pwd     = cfg['app_password']
dir_name    = cfg['dir_path']
from_addr   = cfg['from_addr']
to_addr     = cfg['to_addr']
subject     = cfg['subject']
preview_on  = cfg['preview_on']
video       = cfg['convert_to_video']
send_email  = cfg['send_email']

timestamp   = time.strftime("%b_%d_%Y_%H:%M:%S")
dir_name    = f"{cfg['dir_path']}/{timestamp}"
filepath    = f"{dir_name}/output.mp4"
subject     = f"{cfg['subject']}_{timestamp}"

tuning      = Picamera2.load_tuning_file("imx477_noir.json")
picam2      = Picamera2(tuning=tuning)

picam2.create_preview_configuration()
if preview_on: picam2.start_preview(Preview.QT)

picam2.start()
time.sleep(1)
picam2.set_controls({"AeEnable": 0, "AwbEnable": 0, "FrameRate": 1.0})
time.sleep(1)

os.makedirs(dir_name)

# Take pictures
start_time = time.time()
for i in range(0, photos):
    request = picam2.capture_request()
    time.sleep(photo_delay)
    request.save("main", f"{dir_name}/image{i}.jpg")
    request.release()
    print(f"Captured image {i} of {photos} at {time.time() - start_time:.2f}s")

picam2.stop_preview()
picam2.stop()

if video:
    # convert jpgs to mp4
    os.system(f"ffmpeg -framerate 1 -pattern_type glob -i '{dir_name}/*.jpg' -c:v libx264 -r 30 -pix_fmt yuv420p {dir_name}/output.mp4")

    # Initializing video object
    video_file = MIMEBase('application', "octet-stream")

    # Importing video file
    video_file.set_payload(open(filepath, "rb").read())
    video_file.add_header('content-disposition', 'attachment; filename={}'.format(filepath))

    # Encoding video for attaching to the email
    encoders.encode_base64(video_file)

if send_email:
    # creating EmailMessage object
    msg = MIMEMultipart()

    # Loading message information ---------------------------------------------
    msg['From']     = from_addr
    msg['To']       = to_addr
    msg['Subject']  = f"{subject}_{timestamp}"
    msg['Content']  = timestamp

    msg.attach(video_file)

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login(from_addr, app_pwd)
    server.send_message(msg, from_addr=from_addr, to_addrs=[to_addr])