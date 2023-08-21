import email
import smtplib

from parameters import EMAIL, EMAIL_PASSWORD, congratulations_email, subject_congratulations_email


def string_to_lower(name: str):
    return name.lower()


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
        
    