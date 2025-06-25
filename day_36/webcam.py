import cv2                # Importa la libreria OpenCV per la visione artificiale
import time               # Importa la libreria time per gestire i tempi di attesa

# puoi avere più webcam 0 indica la pricipale se non funziona prova 1 USB
# Crea un oggetto VideoCapture per accedere alla webcam principale (indice 0)
# CAP_DSHOW accelera l’apertura su Windows; ignorato altrove
video = cv2.VideoCapture(0, cv2.CAP_DSHOW)
# Attende 1 secondo prima di iniziare a registrare
time.sleep(1)

while True:                   # Avvia un ciclo infinito per acquisire i frame dalla webcam

    # Legge un frame dalla webcam; check è True se la lettura ha successo, frame contiene l'immagine
    check, frame = video.read()
    # converto il frame in una scala di grigi per avere calcoli + efficienti
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    """
    Applica un filtro gaussiano all’immagine gray_frame, producendo l’uscita gray_frame_gau.
    Kernel (21, 21): finestra quadrata 21×21 pixel; dev’essere dispari per avere un centro definito.
    • σ (sigma) 0: OpenCV calcola automaticamente la deviazione standard in base alla dimensione del kernel.
    • Effetti principali: attenuazione del rumore ad alta frequenza, levigatura dei bordi e preparazione 
    a tecniche come il background subtraction, in cui un’immagine più morbida riduce i falsi positivi.
    """
    gray_frame_gau = cv2.GaussianBlur(gray_frame, (21, 21), 0)

    # Mostra il frame acquisito in una finestra chiamata "My video"
    cv2.imshow("My video", gray_frame_gau)

    # Attende 1 millisecondo la pressione di un tasto e restituisce il codice del tasto premuto
    key = cv2.waitKey(1)

    if key == ord("q"):              # Se viene premuto il tasto "q" (quit)
        break                        # Esce dal ciclo

video.release()                      # Rilascia la
