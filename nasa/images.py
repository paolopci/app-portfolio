import requests as rq


url = "https://apod.nasa.gov/apod/image/2506/Arp273Main_HubblePestana_1080.jpg?" \
    "api_key=TZFNulnLGWpH9bB6Gi7FgHRwVHVQMb2nZMvE4UP2"


def get_image():
    response = rq.get(url)
    with open("image2.jpg", "wb") as file:
        file.write(response.content)
