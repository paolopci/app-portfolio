# -*- coding: utf-8 -*-
"""
overlay_datetime.py
Requisiti:
    pip install opencv-python opencv-contrib-python
    (opencv-contrib porta il modulo cv2.freetype)
    Copiare/fornire un font TrueType con charset UTF-8, es: DejaVuSans.ttf
"""
from datetime import datetime
import cv2
import os
from pathlib import Path

# ------------------------------- #
# 1. Creazione helper: data/ora   #
# ------------------------------- #


def get_datetime_lines(locale: str = "it") -> tuple[str, str]:
    """Restituisce (riga_data, riga_ora) – sempre aggiornate."""
    now = datetime.now()

    if locale.lower().startswith("it"):
        giorni_it = [
            "Lunedì", "Martedì", "Mercoledì",
            "Giovedì", "Venerdì", "Sabato", "Domenica"
        ]
        giorno_settimana = giorni_it[now.weekday()]
    else:
        giorno_settimana = now.strftime("%A")  # es. Monday

    riga_data = f"{giorno_settimana} {now.day:02d}/{now.month:02d}/{now.year}"
    riga_ora = now.strftime("%H:%M:%S")

    return riga_data, riga_ora


# --------------------------------------------------- #
# 2. Disegno robusto (FreeType oppure Hershey+outline) #
# --------------------------------------------------- #
def _load_freetype(font_height: int = 24):
    """Prova a inizializzare il renderer FreeType con un font UTF-8."""
    try:
        ft = cv2.freetype.createFreeType2()
    except AttributeError:
        return None  # modulo non disponibile
    #
    # Path font; scegli il tuo preferito o passalo come argomento.
    # DejaVuSans è comunemente presente su Linux; su Windows puoi usare arial.ttf
    #
    possibles = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        str(Path.home() / "arial.ttf"),
        "./DejaVuSans.ttf"
    ]
    for p in possibles:
        if os.path.isfile(p):
            ft.loadFontData(fontFileName=p, id=0)
            ft.setSplitNumber(0)  # disabilita split multicanale
            return ft
    return None  # nessun font trovato


def draw_datetime_on_frame(
    frame,
    pos_xy: tuple[int, int] = (10, 25),
    font_height: int = 24,
    color_fg=(255, 255, 255),            # bianco
    color_outline=(0, 0, 0),             # nero
    thickness_outline: int = 3,
    locale: str = "it"
):
    """
    Disegna data e ora su `frame` in alto a sinistra, leggibili e non invasive.
    Aggiornare richiamando la funzione ad ogni iterazione del ciclo video.
    """
    riga_data, riga_ora = get_datetime_lines(locale)
    x, y = pos_xy

    # Prova FreeType per supporto UTF-8
    ft = draw_datetime_on_frame._freetype
    if ft:
        # Data con outline
        ft.putText(frame, riga_data, (x, y),
                   fontHeight=font_height,
                   color=color_outline,
                   thickness=thickness_outline,
                   line_type=cv2.LINE_AA,
                   bottomLeftOrigin=False)
        ft.putText(frame, riga_data, (x, y),
                   fontHeight=font_height,
                   color=color_fg,
                   thickness=1,
                   line_type=cv2.LINE_AA,
                   bottomLeftOrigin=False)
        # Ora sotto
        y2 = y + int(font_height * 1.4)
        ft.putText(frame, riga_ora, (x, y2),
                   fontHeight=font_height,
                   color=color_outline,
                   thickness=thickness_outline,
                   line_type=cv2.LINE_AA,
                   bottomLeftOrigin=False)
        ft.putText(frame, riga_ora, (x, y2),
                   fontHeight=font_height,
                   color=color_fg,
                   thickness=1,
                   line_type=cv2.LINE_AA,
                   bottomLeftOrigin=False)
    else:
        # Fallback Hershey: niente accenti (cv2 non li supporta)
        riga_data = riga_data.replace("ì", "i").replace(
            "é", "e").replace("ò", "o")
        scale = font_height / 24.0 * 0.8  # taro la scala sul height desiderato
        font = cv2.FONT_HERSHEY_SIMPLEX

        def put(txt, yy):
            cv2.putText(frame, txt, (x, yy), font, scale,
                        color_outline, thickness_outline, cv2.LINE_AA)
            cv2.putText(frame, txt, (x, yy), font, scale,
                        color_fg, 1, cv2.LINE_AA)

        put(riga_data, y)
        put(riga_ora, y + int(24 * scale * 1.4))


# Caching del renderer FreeType per speed-up
draw_datetime_on_frame._freetype = _load_freetype(font_height=24)
