import smtplib
import ssl

host = "smtp.gmail.com"
port = 465

username = "paolopci@gmail.com"
password = "vrdruiurqwcqbsiw"

receiver = "paolopci@libero.it"
context = ssl.create_default_context()


message = """\
Subject: Test Email prova ..... \
 Ciao Paolo prova invio di un messaggio di prova!!!!!
"""

with smtplib.SMTP_SSL(host, port, context=context) as server:
    server.login(username, password)
    server.sendmail(username, receiver, message)
print("Email sent successfully!")
