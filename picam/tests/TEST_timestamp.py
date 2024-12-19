import time

timestamp = time.strftime("%b_%d_%Y_%H:%M")
dir_name = f"/home/rob/picamera/{timestamp}"
filepath = f"{dir_name}/output.mp4"

print(f"timestamp {timestamp}")
print(f"dir name {dir_name}")
print(f"filepath {filepath}")
# print(f"/home/rob/picamera/{dir_name}")
# print(type(dir_name))
