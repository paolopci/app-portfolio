import smtplib
from email.message import EmailMessage
from pathlib import Path
import filetype
import ssl


def send_email(send_image):
    email_message = EmailMessage()
    email_message["Subject"] = "New customer showed up!"
    # Lettura del file binario
    with open(send_image, "rb") as file:
        content = file.read()

    # Rilevazione del tipo di file
    kind = filetype.guess(content)  # restituisce None se non riconosciuto
    if kind:
        maintype, subtype = kind.mime.split('/')
    else:
        # Fallback sicuro
        maintype, subtype = "application", "octet-stream"

    # Aggiunta dell’allegato (con nome file)
    email_message.add_attachment(
        content,
        maintype=maintype,
        subtype=subtype,
        filename=Path(send_image).name
    )


# send email
host = "smtp.gmail.com"


smtp_port = 465

username = "paolopci@gmail.com"
password = "xorgboyhigeyzvsi"

receiver = "paolopci@libero.it"
context = ssl.create_default_context()

message = """\
Subject: Test Email prova ..... \
 Ciao Paolo prova invio di un messaggio di prova!!!!!
"""

# Invio
context = ssl.create_default_context()
with smtplib.SMTP_SSL(host, smtp_port, context=context) as server:
    server.login(username, password)
    server.send_message(message)
