import customtkinter as ctk
import cv2
from PIL import Image

from services.camera.manager import camera_service
from services.face.service import face_ai
from services.image.face_cropper import FaceCropper



class CameraWidget(ctk.CTkLabel):

    def __init__(self, parent):
        super().__init__(parent, text="")

        self.current_frame = None
        self.current_embedding = None

        self.after(30, self.update_frame)

    def update_frame(self):

        if not self.winfo_exists():
            return

        if camera_service.camera.cap is not None:

            ok, frame = camera_service.camera.read()

            if ok:
                self.current_frame = frame.copy()

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            brightness = gray.mean()

            if brightness < 60:
                frame = cv2.convertScaleAbs(frame, alpha=1.5, beta=40)

            faces = face_ai.detector.detect(frame)
            self.last_face_crop = None

            results = face_ai.recognizer.recognize(frame)

            self.current_embedding = None

            if len(results):
                self.current_embedding = results[0].embedding
            else:
                self.current_embedding = None

            if faces is not None:

                for index, face in enumerate(faces):
                    self.last_face_crop = FaceCropper.crop(
                        frame,
                        face
                    )

                    if index < len(results):

                        embedding = results[index].embedding

                        name, score = face_ai.recognizer.identify(
                            embedding
                        )

                    else:

                        name = "Unknown"
                        score = 0


                    window = self.winfo_toplevel()

                    if (
                        hasattr(window, "check_unknown")
                        and window.winfo_exists()
                    ):
                        window.check_unknown(name)


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
                        (0, 255, 0),
                        2
                    )

            if ok:

                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                image = Image.fromarray(frame)

                image = image.resize((800, 450))

                self.camera_image = ctk.CTkImage(
                    light_image=image,
                    dark_image=image,
                    size=(800, 450)
                )

                self.configure(image=self.camera_image)

        if self.winfo_exists():
            self.after(30, self.update_frame)