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
mp4_name    = cfg['mp4_name']
mail_sever  = cfg['email_server_name']
app_pwd     = cfg['app_password']
dir_name    = cfg['dir_path']
output_dir  = cfg['output_folder']
from_addr   = cfg['from_addr']
to_addrs    = cfg['to_addrs']
preview_on  = cfg['preview_on']
video       = cfg['convert_to_video']
send_email  = cfg['send_email']

# File Setup
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

timestamp   = time.strftime("%b_%d_%Y_%H:%M:%S")
dir_name    = f"{output_dir}{timestamp}/"

os.makedirs(dir_name)

mp4_path    = f"{dir_name}{mp4_name}"

# Camera Setup
tuning      = Picamera2.load_tuning_file("imx477_noir.json")
picam2      = Picamera2(tuning=tuning)

picam2.create_preview_configuration()
if preview_on: picam2.start_preview(Preview.QT)

picam2.start()
time.sleep(1)
picam2.set_controls({"AeEnable": 0, "AwbEnable": 0, "FrameRate": 1.0})
time.sleep(1)

# Take pictures
def takePictures():
    start_time  = time.time()

    for i in range(0, photos):
        request = picam2.capture_request()
        request.save("main", f"{dir_name}/image{i}.jpg")
        request.release()
        print(f"Captured image {i} of {photos} at {time.time() - start_time:.2f}s")
        time.sleep(photo_delay)

    if preview_on: picam2.stop_preview()
    picam2.stop()


# Convert photos to timelapse video
def createVideoFile():
    # convert jpgs to mp4
    os.system(f"ffmpeg -framerate 1 -pattern_type glob -i '{dir_name}/*.jpg' -c:v libx264 -r 30 -pix_fmt yuv420p {mp4_path}")

    # Initializing video object
    video_file = MIMEBase('application', "octet-stream")
    video_file.set_payload(open(mp4_path, "rb").read())
    video_file.add_header('content-disposition', 'attachment; filename={}'.format(mp4_path))

    # Encoding video for attaching to the email
    encoders.encode_base64(video_file)

    return video_file


# Email Video
def emailVideoFile(video_file):
    recipients = ', '.join(to_addrs)

    msg = MIMEMultipart()
    msg['From']     = from_addr
    msg['To']       = recipients
    msg['Subject']  = timestamp
    msg['Content']  = timestamp

    msg.attach(video_file)

    server = smtplib.SMTP(mail_sever, 587)
    server.ehlo()
    server.starttls()
    server.login(from_addr, app_pwd)
    server.send_message(msg, from_addr=from_addr, to_addrs=recipients)


def main():
    takePictures()
    if video: mp4 = createVideoFile()
    if send_email: emailVideoFile(video_file=mp4)


if __name__== "__main__":
    main()