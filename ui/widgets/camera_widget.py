import customtkinter as ctk
import cv2
from PIL import Image, ImageTk

from services.camera.manager import camera_service
# from services.face.service import FaceService

# face_ai = FaceService()


class CameraWidget(ctk.CTkLabel):

    def __init__(self, parent):
        super().__init__(parent, text="")

        self.after(30, self.update_frame)

    def update_frame(self):

        if camera_service.camera.cap is not None:

            ok, frame = camera_service.camera.read()
            # frame = face_ai.detector.detect(frame)

            if ok:

                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                image = Image.fromarray(frame)

                image = image.resize((800, 450))

                photo = ImageTk.PhotoImage(image=image)

                self.configure(image=photo)

                self.image = photo

        self.after(30, self.update_frame)