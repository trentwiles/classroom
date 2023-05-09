from dotenv import load_dotenv
import os
import smtplib
from email.mime.text import MIMEText

load_dotenv()
# Define the email addresses and message details
sender_email = os.getenv("EMAIL")
receiver_email = [os.getenv("TEST_EMAIL")]
password = os.getenv("EMAIL_PASSWORD")



def send_email(subject, body, sender, recipients, password):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = ', '.join(recipients)
    smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    smtp_server.login(sender, password)
    smtp_server.sendmail(sender, recipients, msg.as_string())
    smtp_server.quit()

send_email("whats up", "hey court", send_email, receiver_email, password)