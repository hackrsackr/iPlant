from picamera2 import Picamera2

picam2 = Picamera2()

picam2.start_and_capture_files("timelapses/test{:d}.jpg", initial_delay=2, delay=30, num_files=5)