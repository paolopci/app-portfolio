import cv2
import streamlit as st
from get_datetime_from_video import draw_datetime_on_frame   # modulo sopra

st.title("Motion Detection con data/ora")
if st.button("Start Camera"):
    cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # o semplicemente 0
    stframe = st.image([])

    while cam.isOpened():
        ret, frame = cam.read()
        if not ret:
            st.error("Camera non disponibile")
            break

        # Disegna data+ora (top-left, scala ridotta)
        draw_datetime_on_frame(
            frame,
            pos_xy=(10, 25),      # margine 10 px
            font_height=20,       # dimensione compatta ma leggibile
            color_fg=(255, 255, 255),
            color_outline=(0, 0, 0),
            thickness_outline=2
        )

        stframe.image(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB), channels="RGB")

    cam.release()
