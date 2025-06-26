import requests as rq

api_key = "TZFNulnLGWpH9bB6Gi7FgHRwVHVQMb2nZMvE4UP2"
# url = "https://apod.nasa.gov/apod/image/2506/Arp273Main_HubblePestana_1080.jpg?" \
#     f"api_key={api_key}"


def get_image(url):
    url = url+f"?api_key={api_key}"
    response = rq.get(url)
    with open("image2.jpg", "wb") as file:
        file.write(response.content)
