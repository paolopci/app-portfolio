import cv2
import time
# Per stampare il risultato anche se il programma esce in modo inatteso
import atexit


def main():
    t0 = time.perf_counter()          # Avvio cronometro

    # CAP_DSHOW accelera l’apertura su Windows; ignorato altrove
    cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    if not cam.isOpened():                       # Verifica rapida dell’accesso alla camera
        raise RuntimeError("Impossibile aprire la webcam (indice 0)")

    # Aspetta il primo frame valido
    while True:
        ok, frame = cam.read()
        if ok:
            break
        time.sleep(0.01)               # Alleggerisce il polling della CPU

    warm_up = time.perf_counter() - t0

    # Registrazione stampa a uscita garantita (anche con Ctrl-C)
    def _report():
        print(f"📷  Tempo di attivazione webcam: {warm_up:.2f} s")
    atexit.register(_report)

    # --- ciclo principale ---
    while True:
        cv2.imshow("Preview", frame)
        ok, frame = cam.read()         # Aggiorna il frame
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cam.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
