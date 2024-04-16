import smtplib
from email.mime.text import MIMEText

def send_email(receiver_email: str, subject: str, message: str):
    sender_email = "obsudim.7@mail.ru"
    password = "MySAWsLx6WkitzCanTay"

    msg = MIMEText(message)
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = receiver_email

    server = smtplib.SMTP_SSL('smtp.mail.ru', 465)
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, msg.as_string())
    server.quit()