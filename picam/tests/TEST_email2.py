import smtplib
import json
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart

with open('config.json', 'r') as f:
    cfg = json.load(f)

from_addr = 'rob.knighton10@gmail.com'
to_addr = 'mastersmc23@gmail.com'
subject = 'I just sent this email from Python!'
content = 'Test'
filepath = "/home/rob/iPlant/picam/timelapses/Jan_02_2025_18:42:00/timelapse.mp4" 

# Initializing video object
video_file = MIMEBase('application', "octet-stream")

# Importing video file
video_file.set_payload(open(filepath, "rb").read())
video_file.add_header('content-disposition', 'attachment; filename={}'.format(filepath))

# Encoding video for attaching to the email
encoders.encode_base64(video_file)

# creating EmailMessage object
msg = MIMEMultipart()

# Loading message information ---------------------------------------------
msg['From'] = "rob.knighton10@gmail.com"
msg['To'] = 'mastersmc23@gmail.com'
msg['Subject'] = 'text for the subject line'
# msg.set_content('text that will be in the email body.')
msg.attach(video_file)

server = smtplib.SMTP('smtp.gmail.com', 587)
server.ehlo()
server.starttls()
server.login(from_addr, cfg['app_password'])
server.send_message(msg, from_addr=from_addr, to_addrs=to_addr)