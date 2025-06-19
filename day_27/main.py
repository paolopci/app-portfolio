
from send_email2 import send_email
import requests


url = "https://newsapi.org/v2/everything?q=tesla&from=2025-05-19&sortBy=publishedAt&apiKey=2f4bc007f9094545b72fb6a4a37be75d"


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
}

req = requests.get(url, headers=headers)
content = req.json()


icount = 0
for item in content['articles']:
    # print(item['title'])
    # print(item['description'])
    message = item['description']
    oggetto = item['title']
    destinatario = "paolopci@libero.it"
    if icount < 5:
        send_email(message, oggetto, "paolopci@libero.it")
        icount += 1
        print(f"{icount} - email invia a : {destinatario}")
