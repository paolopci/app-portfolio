# import requests
# import selectorlib
import service as sc
import time


URL = "https://programmer100.pythonanywhere.com/tours/"


while True:

    scraped = sc.scrape(URL)
    extracted = sc.extract(scraped)
    print(extracted)

    if extracted != "No upcoming tours" and sc.is_new(extracted):
        sc.store(extracted)
        sc.send_email(extracted)
    time.sleep(1)
