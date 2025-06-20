from email.message import EmailMessage
import ssl
import smtplib
import os


# def send_email(sender, password, receiver, subject, body):
def send_email(message, subject, user_email):
    host = "smtp.gmail.com"
    port = 465
    sender = "paolopci@gmail.com"
    password = os.getenv("PASSWORD")  # Use environment variable for security
    receiver = user_email

    em = EmailMessage()
    em['From'] = sender
    em['To'] = user_email
    em['Subject'] = subject
    em.set_content(message)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL(host, port, context=context) as smtp:
        smtp.login(sender, password)
        smtp.sendmail(sender, receiver, em.as_string())
        print("Email sent successfully!")


# send_email('Ciao Paolo', 'Saluto', 'paolopci@libero.it')
