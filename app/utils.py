import email
import smtplib
from passlib.context import CryptContext

from app.parameters import EMAIL, EMAIL_PASSWORD, congratulations_email, subject_congratulations_email

crypt = CryptContext(schemes=['bcrypt'])



def create_hash(password):
    return crypt.hash(password)

def validate_password(password_hash, password):
    return crypt.verify(password, password_hash)

def string_to_lower(name: str):
    return name.lower()

def fix_video_link(link_video: str):
    link_fixed = link_video.replace("watch?v=", "embed/")
    return link_fixed

def send_email(employee_email, email_body, email_subject):
    
    msg = email.message.Message()
    msg['Subject'] = email_subject
    msg['From'] = EMAIL
    msg['To'] = employee_email
    password = EMAIL_PASSWORD
    msg.add_header('Content-Type', 'text/html')
    msg.set_payload(email_body)

    if password:
        s = smtplib.SMTP('smtp.gmail.com: 587')
        s.starttls()
        s.login(msg['From'], password)
        s.sendmail(msg['From'], [msg['To']], msg.as_string().encode('utf-8'))
