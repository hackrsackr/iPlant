import time

from picamera2 import Picamera2, Preview

cam = Picamera2()
cam.start_preview(Preview.QT)
preview_config = cam.create_preview_configuration(main={"size":(400, 280)})
cam.configure(preview_config)

cam.start()
time.sleep(10)
