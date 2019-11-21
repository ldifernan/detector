from gpiozero import MotionSensor, LED
from email.mime.multipart import MIMEMultipart
import smtplib
import logging

## VARS

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
    s.send_message(msg)
    logging.info("Email sent to " + mail)
    del msg
    s.quit()

## MAIN


logging.basicConfig(filename='detector.log', filemode='w', format=log_format,
    datefmt=log_date_format, level=log_level)
led.off()
while True:
    pir.wait_for_motion()
    logging.info("Motion Detected")
    send_mail()
    led.on()
    pir.wait_for_no_motion()
    led.off()
