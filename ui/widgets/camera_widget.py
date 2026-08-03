import customtkinter as ctk
import cv2
from PIL import Image, ImageTk

from services.camera.manager import camera_service
from services.face.service import face_ai
from services.face.trainer import face_trainer
# from services.face.service import FaceService

# face_ai = FaceService()


class CameraWidget(ctk.CTkLabel):

    def __init__(self, parent):
        super().__init__(parent, text="")

        self.current_frame = None

        self.bind("<KeyPress-r>", self.register_face)
        self.focus_set()

        self.after(30, self.update_frame)

    def update_frame(self):

        if camera_service.camera.cap is not None:

            ok, frame = camera_service.camera.read()

            if ok:
                self.current_frame = frame.copy()

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            brightness = gray.mean()

            if brightness < 60:
                frame = cv2.convertScaleAbs(frame, alpha=1.5, beta=40)

            faces = face_ai.detector.detect(frame)

            if faces is not None:

                for face in faces:
                    results = face_ai.recognizer.recognize(frame)

                    if len(results):

                        name, score = face_ai.recognizer.identify(
                            results[0].embedding
                        )

                    else:

                        name = "Unknown"
                        score = 0

                    x, y, w, h = face[:4].astype(int)

                    cv2.rectangle(
                        frame,
                        (x, y),
                        (x + w, y + h),
                        (0, 255, 0),
                        2
                    )

                    cv2.putText(
                        frame,
                        f"{name}  {score:.2f}",
                        (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.7,
                        (0,255,0),
                        2
                    )
            # frame = face_ai.detector.detect(frame)

            if ok:

                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                image = Image.fromarray(frame)

                image = image.resize((800, 450))

                photo = ImageTk.PhotoImage(image=image)

                self.configure(image=photo)

                self.image = photo

        self.after(30, self.update_frame)

    def register_face(self, event=None):

        print("R pressed")

        frame = self.current_frame

        if frame is None:
            print("No current frame")
            return

        success = face_trainer.register(frame, "Manav")

        if success:
            print("✅ Manav Registered")
        else:
            print("❌ Face not detected")