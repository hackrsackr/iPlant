#!/usr/bin/python3
import json
import os
import shutil
import subprocess
import time
import smbus2
import bme280

from smtplib import SMTP
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart

from picamera2 import Picamera2, Preview
from PIL import Image, ImageDraw, ImageFont
from schedule import every, repeat, run_pending

from BME280 import getTempAndHumidity

with open('config.json', 'r') as f:
    cfg = json.load(f)

photos: int         = cfg['number_of_photos']
photo_delay: int    = cfg['secs_between_photos']
fps: int            = cfg['frames_per_second']
script_time: str    = cfg['execute_script_time']
mp4_name: str       = cfg['mp4_name']
mail_sever: str     = cfg['mail_server']
app_pwd: str        = cfg['app_password']
output_dir: str     = cfg['output_folder']
from_addr: str      = cfg['from_addr']
to_addrs: list      = cfg['to_addrs']
subject: str        = cfg['subject']
preview_on: bool    = cfg['preview_on']
make_video: bool    = cfg['convert_to_video']
send_email: bool    = cfg['send_email']

# Camera setup
picam2: Picamera2   = Picamera2(tuning=Picamera2.load_tuning_file("imx477.json"))
config: dict        = picam2.create_preview_configuration()
preview: Preview    = Preview.QT if preview_on else Preview.NULL

picam2.start(config=config, show_preview=preview) 

# BME280 setup
port: int = 1
address: str = 0x76
bus = smbus2.SMBus(port)
calibration_params = bme280.load_calibration_params(bus, address)


def getTimestamp() -> str:
    """Returns times stamp used for album name"""
    timestamp: str = time.strftime("%b_%d_%Y_%H:%M:%S")

    return timestamp


def getAlbumName(timestamp: str) -> str:
    """Returns name of the main directory for images and video"""
    album_name: str = f"{output_dir}/{timestamp}/"

    return album_name


def getMP4Path(album_name: str) -> str:
    """Returns file path of video file"""
    mp4_path: str = f"{album_name}{mp4_name}"

    return mp4_path


def takePictures(album_name: str) -> None:
    """Take Pictures for timelapse series"""

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    os.makedirs(album_name)
    os.makedirs(f"{album_name}images")

    start_time: float   = time.time()
    image_font: object  = ImageFont.truetype('FreeMono', 18)
    image_fill: object  = (255, 255, 255)

    for i in range(0, photos):
        image_num: int  = f"{i + 1:03d}"
        image_path: str = f"{album_name}/images/image{image_num}.jpg"
        image_text: str = f"image: {image_num}"

        temperature, humidity = getTempAndHumidity()
        
        request: None   = picam2.capture_request()
        request.save("main", image_path)
        request.release()
        print(f"Captured image {image_num} of {photos} at {time.time() - start_time:.2f}s")
        
        img: object = Image.open(image_path)
        draw: object = ImageDraw.Draw(img, mode="RGBA")
        os.remove(image_path)

        draw.text((10, 320), time.strftime("%b_%d_%Y"), font=image_font, fill=image_fill)
        draw.text((10, 340), time.strftime("%H:%M:%S"), font=image_font, fill=image_fill)
        draw.text((10, 360), f"Temp: {temperature:.1f}°f", font=image_font, fill=image_fill)
        draw.text((10, 380), f"Humid: {humidity:.1f}%", font=image_font, fill=image_fill)
        img.save(image_path)

        time.sleep(photo_delay)


def createVideo(album_name: str, mp4_path: str, input_pattern: str, output_file: str, fps: int=30, pix_fmt: str='yuv420p', codec: str='libx264') -> MIMEBase:
    """Creates a timelapse video from the images."""

    # FFMPEG command 
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

    video_file: MIMEBase = MIMEBase('application', 'octet-stream')
    video_file.set_payload(open(mp4_path, "rb").read())
    video_file.add_header('content-disposition', 'attachment; filename={}'.format(mp4_path))

    # Delete images file
    shutil.rmtree(f"{album_name}images")

    return video_file


def sendEmail(video_file: MIMEBase, timestamp: str) -> None:
    """Email video file"""

    # Encoding video for attaching to the email
    encoders.encode_base64(video_file)

    recipients: str     = ', '.join(to_addrs)

    msg: MIMEMultipart  = MIMEMultipart()
    msg['From']         = from_addr
    msg['To']           = recipients
    msg['Subject']      = subject
    msg['Content']      = timestamp

    msg.attach(video_file)

    server: SMTP = SMTP(mail_sever, 587)
    server.ehlo()
    server.starttls()
    server.login(from_addr, app_pwd)
    server.send_message(msg, from_addr=from_addr, to_addrs=recipients)


@repeat(every().day.at(script_time))
def sendTimelapse() -> None:    
    """
    Take images based on config.json inputs
    Creates timelapse video file out of images
    Sends timelapse video by email
    """

    timestamp = getTimestamp()
    album_name = getAlbumName(timestamp)
    mp4_path = getMP4Path(album_name)

    takePictures(album_name)

    if make_video:
        video_file = createVideo(
            album_name      = album_name,
            mp4_path        = mp4_path,
            input_pattern   = f"{album_name}/images/image*.jpg",
            output_file     = mp4_path, 
            fps             = fps
        )
    
    if send_email:
        sendEmail(video_file, timestamp)


def main() -> None:    
    while True:
        run_pending()


if __name__== "__main__":
    # DEBUG: bool = True
    DEBUG: bool = False

    if DEBUG:
        sendTimelapse()
    
    else:
        main()

