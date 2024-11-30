import os
import datetime

path = str(datetime.date.today())
print("Current working directory:", os.getcwd())

os.chdir("/home/rob/picamera/" + path)
os.system("ffmpeg -framerate 1 -pattern_type glob -i '*.jpg' -c:v libx264 -r 30 -pix_fmt yuv420p output.mp4")