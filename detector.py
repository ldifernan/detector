from gpiozero import MotionSensor, LED
from email.mime.multipart import MIMEMultipart
import smtplib

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
    print("login succesful")
    msg = MIMEMultipart()
    msg['From'] = mail_from
    msg['To'] = mail_to
    msg['Subject'] = mail_subject
    s.send_message(msg)
    print("email sent")
    del msg
    s.quit()


while True:
    pir.wait_for_motion()
    print("Motion Detected!")
    send_mail()
    led.on()
    pir.wait_for_no_motion()
    led.off()
