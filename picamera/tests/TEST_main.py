#!/usr/bin/python3
import json
import os
# import schedule
import shutil
import subprocess
import time

from smtplib import SMTP
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart

from picamera2 import Picamera2, Preview
from PIL import Image, ImageDraw, ImageFont
# from schedule import every, repeat, run_pending

# Config
with open('config.json', 'r') as f:
    cfg = json.load(f)

photos: int         = cfg['number_of_photos']
photo_delay: int    = cfg['secs_between_photos']
mp4_name: str       = cfg['mp4_name']
mail_sever: str     = cfg['email_server_name']
app_pwd: str        = cfg['app_password']
output_dir: str     = cfg['output_folder']
from_addr: str      = cfg['from_addr']
to_addrs: list      = cfg['to_addrs']
preview_on: bool    = cfg['preview_on']
video: bool         = cfg['convert_to_video']
send_email: bool    = cfg['send_email']

timestamp: str      = time.strftime("%b_%d_%Y_%H:%M:%S")
album_name: str     = f"{output_dir}{timestamp}/"
mp4_path: str       = f"{album_name}{mp4_name}"

def create_timelapse(input_pattern, output_file, fps: int=30, pix_fmt: str='yuv420p', codec: str='libx264') -> MIMEBase:
    """Takes Pictures and creates a timelapse video from the images."""
    
    # Folder Setup 
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    os.makedirs(album_name)
    os.makedirs(f"{album_name}images")

    # Take Pictures
    picam2: Picamera2   = Picamera2(tuning=Picamera2.load_tuning_file("imx477_noir.json"))
    config: dict        = picam2.create_preview_configuration()
    preview: Preview    = Preview.QT if preview_on else Preview.NULL

    picam2.start(config=config, show_preview=preview)
    
    start_time: float   = time.time()
    image_font: ImageFont = ImageFont.truetype('FreeMono', 18)

    for i in range(0, photos):
        image_num: int  = i + 1
        image_path: str = f"{album_name}/images/image{image_num}.jpg"
        image_text: str = "var_string"
        request: None   = picam2.capture_request()
        request.save("main", image_path)
        request.release()
        print(f"Captured image {image_num} of {photos} at {time.time() - start_time:.2f}s")
        img = Image.open(image_path)
        draw = ImageDraw.Draw(img)
        os.remove(image_path)
        draw.text((10, 30), image_text, font=image_font, fill=(255, 255, 255))
        draw.text((10, 50), image_text, font=image_font, fill=(255, 255, 255))
        img.save(image_path)

        time.sleep(photo_delay)

    picam2.stop()

    # Create Timelapse video
    cmd: list = [
        'ffmpeg',
        '-r', str(fps),             # Set the desired frame rate for the output video
        '-pattern_type', 'glob',    # Use glob pattern matching for input files
        '-i', input_pattern,        # Input image pattern (e.g., '*.jpg')
        '-c:v', codec,              # Specify the video codec (e.g., libx264, h265)
        '-pix_fmt', pix_fmt,        # Set the pixel format (e.g., yuv420p)
        output_file                 # Output video file
    ]
    subprocess.run(cmd)

    video_file: MIMEBase = MIMEBase('application', "octet-stream")
    video_file.set_payload(open(mp4_path, "rb").read())
    video_file.add_header('content-disposition', 'attachment; filename={}'.format(mp4_path))

    shutil.rmtree(f"{album_name}images")

    return video_file


def emailTimelapse(video_file: MIMEBase) -> None:
    ''' Create video file object and encode it for attaching to email'''

    # Encoding video for attaching to the email
    encoders.encode_base64(video_file)

    recipients: str     = ', '.join(to_addrs)

    msg: MIMEMultipart  = MIMEMultipart()
    msg['From']         = from_addr
    msg['To']           = recipients
    msg['Subject']      = timestamp
    msg['Content']      = timestamp

    msg.attach(video_file)

    server: SMTP = SMTP(mail_sever, 587)
    server.ehlo()
    server.starttls()
    server.login(from_addr, app_pwd)
    server.send_message(msg, from_addr=from_addr, to_addrs=recipients)

# @schedule.repeat(schedule.every(3).minutes)
def main() -> None:
    vid: MIMEBase       = create_timelapse(
        input_pattern   = f"{album_name}/images/image*.jpg", 
        output_file     = mp4_path, 
        fps             = 1, 
        pix_fmt         = 'yuv420p', 
        codec           = 'libx264')

    if send_email: emailTimelapse(vid)

    # while True:
    #     schedule.run_pending()
    #     time.sleep(1)


if __name__== "__main__":
    main()