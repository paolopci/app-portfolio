
from send_email2 import send_email
import requests

topic = "tesla"
url = f"https://newsapi.org/v2/everything?q={topic}&" \
    "from=2025-05-19&" \
    "sortBy=publishedAt&" \
    "apiKey=2f4bc007f9094545b72fb6a4a37be75d&" \
    "language=en"  # solo quelli in lingua inglese


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
}

req = requests.get(url, headers=headers)
content = req.json()

body = ''
icount = 0
for item in content['articles'][:20]:
    description = item.get(
        'description') or "Nessuna descrizione disponibile."+"\n"
    body += description+"\n" + \
        item.get('url') or "Nessun URL disponibile."+2*"\n"


message = body
oggetto = item['title']
destinatario = "paolopci@libero.it"
send_email(message, oggetto, "paolopci@libero.it")
