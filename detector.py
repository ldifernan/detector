from gpiozero import MotionSensor, LED
from email.mime.multipart import MIMEMultipart
import smtplib
import logging

logging.basicConfig(filename='detector.log', filemode='w', format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')
pir = MotionSensor(4)
led = LED(3)
mail = "xxxx@xxx.com"
password = "xxxxxx"
smtp_host = "smtp-mail.outlook.com"
smtp_port = 587
mail_from = "xxxx@xxx.com"
mail_to = "yyyy@yyy.com"
mail_subject = "Presence detected"
led.off()


def send_mail():
    s = smtplib.SMTP(host=smtp_host, port=smtp_port)
    s.starttls()
    s.login(mail, password)
    logging.info("Login succesful")
    msg = MIMEMultipart()
    msg['From'] = mail_from
    msg['To'] = mail_to
    msg['Subject'] = mail_subject
    s.send_message(msg)
    logging.info("Email sent to " + mail)
    del msg
    s.quit()


while True:
    pir.wait_for_motion()
    logging.info("Motion Detected")
    send_mail()
    led.on()
    pir.wait_for_no_motion()
    led.off()
