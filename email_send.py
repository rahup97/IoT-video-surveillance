from email.mime.text import MIMEText
import smtplib

def warning_email(name, email, time_of_motion):
    from_email = "<email>"
    from_password = "<pass>"
    to_email = email

    subject = "WARNING: MOTION DETECTED!"
    message = "Hello <strong>%s</strong>,<br><br> An unexpected motion was detected in your room at time: <strong>%s</strong>." %(name, time_of_motion)

    msg = MIMEText(message, 'html')
    msg['Subject'] = subject
    msg['To'] = to_email
    msg['From'] = from_email

    gmail = smtplib.SMTP('smtp.gmail.com', 587)
    gmail.ehlo()
    gmail.starttls()
    gmail.login(from_email, from_password)
    gmail.send_message(msg)
