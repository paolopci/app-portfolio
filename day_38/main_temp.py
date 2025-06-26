import service_temp as sc
import time


URL = "https://programmer100.pythonanywhere.com/"

while True:

    scraped = sc.scrape(URL)
    extracted = sc.extract(scraped)
    sc.store(extracted)
    print(f"Nuova temperatura salvata. {extracted}°C")

    time.sleep(1)
