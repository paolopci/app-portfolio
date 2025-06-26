import requests
import selectorlib
from pathlib import Path
import smtplib
import ssl
from datetime import datetime

HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/138.0.0.0 Safari/537.36'
}

URL = "https://programmer100.pythonanywhere.com/"

# Directory in cui si trova questo script (es. app1/day_38)
BASE_DIR = Path(__file__).resolve().parent
DEFAULT_STORE = BASE_DIR / "data_temp.txt"


def scrape(url: str) -> str:
    """Restituisce il sorgente HTML della pagina indicata."""
    response = requests.get(url, headers=HEADERS, timeout=15)
    response.raise_for_status()
    return response.text


def extract(source: str) -> str:
    """Estrae la temperatura dal sorgente HTML usando selectorlib."""
    extractor = selectorlib.Extractor.from_yaml_file("extract_temp.yaml")
    value = extractor.extract(source)["temperature"]
    return value


def send_email(evento: str) -> None:
    """Invia un'email con il nuovo evento."""
    host = "smtp.gmail.com"
    port = 465
    username = "paolopci@gmail.com"
    password = "vrdruiurqwcqbsiw"  # ⚠️ Tenere credenziali al sicuro
    receiver = "paolopci@libero.it"

    context = ssl.create_default_context()
    message = (
        "Subject: Nuova lettura temperatura\n\n"
        "Ciao Paolo,\n\n"
        "È stata registrata una nuova temperatura:\n\n"
        f"{evento}\n"
    )

    with smtplib.SMTP_SSL(host, port, context=context) as server:
        server.login(username, password)
        server.sendmail(username, receiver, message)

    print("Email inviata correttamente!")


def _ensure_file_with_header(path: Path) -> None:
    """Crea il file se non esiste e scrive l'intestazione."""
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)  # assicura la cartella
        with path.open("w", encoding="utf-8") as f:
            f.write("date,temperature\n")


def is_new(event: str, store_path: Path = DEFAULT_STORE) -> bool:
    """Ritorna *True* se *event* non è già nel file CSV, *False* altrimenti."""
    _ensure_file_with_header(store_path)

    with store_path.open("r", encoding="utf-8") as f:
        next(f)  # salta intestazione
        return event not in (
            line.rstrip("\n").split(",")[-1]
            for line in f
        )


def store(new_event: str, store_path: Path = DEFAULT_STORE) -> None:
    """Accoda una nuova riga `yy-mm-dd-hh-mm-ss,temperatura` al CSV."""
    _ensure_file_with_header(store_path)

    timestamp = datetime.now().strftime("%y-%m-%d-%H-%M-%S")
    record = f"{timestamp},{new_event}"

    with store_path.open("a", encoding="utf-8") as f:
        f.write(record + "\n")


if __name__ == "__main__":
    html = scrape(URL)
    temperature = extract(html)
    print(f"Temperatura estratta: {temperature}")

    was_new = is_new(temperature)  # controllo duplicato solo per email
    store(temperature)             # APPEND SEMPRE, anche se già presente

    if was_new:
        #   send_email(temperature)
        print("Nuova temperatura salvata.")
    else:
        print("Temperatura già presente; lettura salvata ugualmente.")
