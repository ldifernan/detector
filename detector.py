from picamera import PiCamera
from gpiozero import MotionSensor, LED
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib
import logging
import time
from datetime import datetime

## VARS


now = datetime.now()
timestr = now.strftime("%Y%m%d-%H%M%S")
picture = "/home/pi/detector/" + timestr + ".jpg"
pir = MotionSensor(4)
led = LED(3)
mail = "xxxx@xxx.com"
password = "xxxxxx"
smtp_host = "smtp-mail.outlook.com"
smtp_port = 587
mail_from = "xxxx@xxx.com"
mail_to = "yyyy@yyy.com"
mail_subject = "Presence detected"
log_format = '%(asctime)s - %(message)s'
log_date_format = '%d-%b-%y %H:%M:%S'
log_level = logging.INFO
camera = PiCamera()

## FUNCTIONS


def send_mail():
    s = smtplib.SMTP(host=smtp_host, port=smtp_port)
    s.starttls()
    s.login(mail, password)
    logging.debug("Login succesful")
    msg = MIMEMultipart()
    msg['From'] = mail_from
    msg['To'] = mail_to
    msg['Subject'] = mail_subject
    # string to store the body of the mail
    body = "Presence detected"
    # attach the body with the msg instance
    msg.attach(MIMEText(body, 'plain'))
    # open the file to be sent
    #filename = timestr + ".h264"
    #attachment = open("/home/pi/detector/video" + filename, "rb")
    filename = timestr + ".jpg"
    attachment = open("/home/pi/detector/" + filename, "rb")
    # instance of MIMEBase and named as p
    p = MIMEBase('application', 'octet-stream')
    # To change the payload into encoded form
    p.set_payload((attachment).read())
    # encode into base64
    encoders.encode_base64(p)
    p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
    # attach the instance 'p' to instance 'msg'
    msg.attach(p)
    s.send_message(msg)
    logging.info("Email sent to " + mail_to)
    del msg
    s.quit()


def take_photo():
    camera.start_preview()
    time.sleep(3)
    camera.capture('/home/pi/detector/' + timestr + '.jpg')
    camera.stop_preview()


def capture_video():
    camera.start_preview()
    camera.start_recording('/home/pi/detector/video' + timestr + '.h264')
    time.sleep(5)
    camera.stop_recording()
    camera.stop_preview()

## MAIN


logging.basicConfig(filename='detector.log', filemode='a', format=log_format,
                    datefmt=log_date_format, level=log_level)

while True:
    pir.wait_for_motion()
    logging.info("Motion Detected")
    led.on()
    take_photo()
    send_mail()
    pir.wait_for_no_motion()
    led.off()
    time.sleep(30)
