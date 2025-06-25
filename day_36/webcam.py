"""Rilevamento movimento tramite webcam.
Premi 'q' per uscire."""

import cv2      # Libreria visione artificiale
import time     # Funzioni di temporizzazione

first_frame = None              # Fotogramma di riferimento

# 0 = webcam predefinita; CAP_DSHOW velocizza l'apertura su Windows
video = cv2.VideoCapture(0, cv2.CAP_DSHOW)

time.sleep(1)                   # Stabilizzazione sensore

while True:
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
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    cv2.imshow("Video", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

video.release()      # Rilascia la webcam
cv2.destroyAllWindows()
