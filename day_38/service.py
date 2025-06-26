import requests
import selectorlib
from pathlib import Path
import smtplib
import ssl


HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36'
}


def scrape(url):
    """ Scrape the page source from the URL"""
    response = requests.get(url, headers=HEADERS)
    source = response.text
    return source


def extract(source):
    extractor = selectorlib.Extractor.from_yaml_file("extract.yaml")
    value = extractor.extract(source)["tours"]
    return value


def send_email(evento):
    host = "smtp.gmail.com"
    port = 465
    username = "paolopci@gmail.com"
    password = "vrdruiurqwcqbsiw"
    receiver = "paolopci@libero.it"
    context = ssl.create_default_context()

    message = f"""Subject: Test Email prova ..... 

    Ciao Paolo nuovo evento della tua banda musicale: 
    
    {evento}
"""

    with smtplib.SMTP_SSL(host, port, context=context) as server:
        server.login(username, password)
        server.sendmail(username, receiver, message)
    print("Email sent successfully!")


def store(new_event):
    with open("data.txt", "a", encoding="utf-8") as file:
        file.write(new_event+"\n")


def is_new(event, store_path="data.txt") -> bool:
    """
    Restituisce True se 'event' non è già presente nel file,
    altrimenti False.
    """
    p = Path(store_path)
    if not p.exists():
        return True                       # primo avvio: file inesistente

    with p.open("r", encoding="utf-8") as f:
        # confronta riga per riga rimuovendo \n e spazi extra
        return event not in (line.rstrip("\n") for line in f)


if __name__ == "__main__":
    scraped = scrape("https://programmer100.pythonanywhere.com/tours/")
    extracted = extract(scraped)
    print(extracted)
    # store(extracted)
    if extracted != "No upcoming tours" and is_new(extracted):
        store(extracted)
        send_email(extracted)
