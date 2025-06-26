"""Rilevamento movimento tramite webcam.
Premi 'q' per uscire."""

import cv2      # Libreria visione artificiale
import time     # Funzioni di temporizzazione
from emailing import send_email
import glob
pww = "vrdruiurqwcqbsiw"
first_frame = None              # Fotogramma di riferimento
status_list = []
count = 1

# 0 = webcam predefinita; CAP_DSHOW velocizza l'apertura su Windows
video = cv2.VideoCapture(0, cv2.CAP_DSHOW)

time.sleep(1)                   # Stabilizzazione sensore

while True:
    status = 0
    ret, frame = video.read()   # Acquisizione frame

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)      # Scala di grigi
    blur = cv2.GaussianBlur(gray, (21, 21), 0)          # Riduzione rumore

    if first_frame is None:
        first_frame = blur
        continue                # Salta il primo ciclo

    # Differenza col background
    delta = cv2.absdiff(first_frame, blur)
    thresh = cv2.threshold(delta, 45, 255, cv2.THRESH_BINARY)[1]
    thresh = cv2.dilate(thresh, None, iterations=2)     # Riempie i buchi

    cv2.imshow("Movimento", thresh)

    contours, _ = cv2.findContours(
        thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for c in contours:
        if cv2.contourArea(c) < 5_000:                  # Rumore trascurabile
            continue
        x, y, w, h = cv2.boundingRect(c)
        rectangle = cv2.rectangle(
            frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
        if rectangle.any():
            status = 1
            cv2.imwrite(f"images/{count}.png", frame)
            count = count+1
            all_images = glob.glob("images/*.png")
            # tra tutte le images che ho salvato prendo una in mezzo
            index = int(len(all_images) / 2)
            image_with_object = all_images[index]

    status_list.append(status)
    status_list = status_list[-2:]
    if status_list[0] == 1 and status_list[1] == 0:
        send_email(image_with_object)

    print(status_list)

    cv2.imshow("Video", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

video.release()      # Rilascia la webcam
cv2.destroyAllWindows()
