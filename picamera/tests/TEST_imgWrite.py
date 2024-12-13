
#!/usr/bin/python3
import time
import json
import os

from picamera2 import Picamera2, Preview

# Importing the PIL library
from PIL import Image, ImageDraw, ImageFont

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

picam2: Picamera2   = Picamera2(tuning=Picamera2.load_tuning_file("imx477_noir.json"))
config: dict        = picam2.create_preview_configuration()
preview: Preview    = Preview.QT if preview_on else Preview.NULL

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

os.makedirs(album_name)
picam2.start(config=config, show_preview=preview)
start_time: float   = time.time()

# Capture Image
image_num: int = 0
request: None = picam2.capture_request()
request.save("main", f"{album_name}/input{image_num}.jpg")
request.release()
print(f"Captured image {image_num} of {photos} at {time.time() - start_time:.2f}s")
img = Image.open(f"{album_name}/input{image_num}.jpg")
draw = ImageDraw.Draw(img)
img.save(f"{album_name}/input{image_num}.jpg")
time.sleep(photo_delay)
 
# Custom font style and font size
text = "Hello, World!"
font = ImageFont.truetype("FreeMono.ttf", 50)
text_color = (255, 255, 255) # white
text_position = (10, 10) # Position (x, y)

# Add Text to an image
draw.text(text_position, text, font=font, fill=text_color)
 
# Display edited image
# img.show()
 
# Save the edited image
# img.save("timelapses/output0.jpg")
 

