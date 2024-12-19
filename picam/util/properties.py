from picamera2 import Picamera2

picam2 = Picamera2()
properties = picam2.camera_properties
print(properties)