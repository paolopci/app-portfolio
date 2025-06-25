import cv2
import time


# puoi avere più webcam 0 indica la pricipale se non funziona prova 1 USB
video = cv2.VideoCapture(0)
check, frame = video.read()  # un frame= immagine 1
time.sleep(1)
check2, frame2 = video.read()  # un frame= immagine 2
time.sleep(1)
check3, frame3 = video.read()  # un frame= immagine 3

print(check)
print(frame)


# Prova ad aprire webcam fino a un massimo di 5 dispositivi
# for index in range(5):
#     video = cv2.VideoCapture(index)
#     check, frame = video.read()
#     if check:
#         print(f"Webcam trovata all'indice {index}")
#         print(frame)
#         video.release()
#         break
#     video.release()
# else:
#     print("Nessuna webcam disponibile.")
