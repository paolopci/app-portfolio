import cv2                # Importa la libreria OpenCV per la visione artificiale
import time               # Importa la libreria time per gestire i tempi di attesa

# puoi avere più webcam 0 indica la pricipale se non funziona prova 1 USB
# Crea un oggetto VideoCapture per accedere alla webcam principale (indice 0)
video = cv2.VideoCapture(0)
# Attende 1 secondo prima di iniziare a registrare
time.sleep(1)

while True:                   # Avvia un ciclo infinito per acquisire i frame dalla webcam

    # Legge un frame dalla webcam; check è True se la lettura ha successo, frame contiene l'immagine
    check, frame = video.read()
    # Mostra il frame acquisito in una finestra chiamata "My video"
    cv2.imshow("My video", frame)

    # Attende 1 millisecondo la pressione di un tasto e restituisce il codice del tasto premuto
    key = cv2.waitKey(1)

    if key == ord("q"):              # Se viene premuto il tasto "q" (quit)
        break                        # Esce dal ciclo

video.release()                      # Rilascia la
