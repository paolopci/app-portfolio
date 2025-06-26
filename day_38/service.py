import requests
import selectorlib

HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36'
}


def scrape(url):
    """ Scrape the page source from the URL"""
    response = requests.get(url, headers=HEADERS)
    source = response.text
    return source


if __name__ == "__main__":
    print(scrape("https://programmer100.pythonanywhere.com/tours/"))
