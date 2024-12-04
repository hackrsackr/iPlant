
#!/usr/bin/python3
import time
import json
# import os
import smtplib

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart

# from picamera2 import Picamera2, Preview

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

timestamp   = time.strftime("%b_%d_%Y_%H:%M:%S")

if send_email:
    msg = MIMEMultipart()

    recipients = ', '.join(to_addrs)

    msg['From']     = from_addr
    msg['To']       = recipients
    msg['Subject']  = timestamp
    msg['Content']  = timestamp

    # msg.attach(video_file)

    server = smtplib.SMTP(mail_sever, 587)
    server.ehlo()
    server.starttls()
    server.login(from_addr, app_pwd)
    server.send_message(msg, from_addr=from_addr, to_addrs=recipients)