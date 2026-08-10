"""
Camera Widget
Recognition System v2
"""

import time

import cv2
import customtkinter as ctk
from PIL import Image

from services.camera.manager import camera_service
from services.face.service import face_ai
from services.image.face_cropper import FaceCropper
from services.unknown_queue.queue_service import unknown_queue


class CameraWidget(ctk.CTkLabel):

    def __init__(self, parent):

        super().__init__(parent, text="")

        self.current_frame = None
        self.current_embedding = None
        self.last_face_crop = None

        self.fps = 0
        self.frame_counter = 0
        self.last_time = time.time()

        self.after(30, self.update_frame)

    # =======================================================
    # Main Loop
    # =======================================================

    def update_frame(self):

        if not self.winfo_exists():
            return

        try:

            if camera_service.camera.cap is None:
                self.after(100, self.update_frame)
                return

            ok, frame = camera_service.camera.read()

            if not ok or frame is None:
                self.after(30, self.update_frame)
                return

            self.current_frame = frame.copy()

            # ------------------------------------------
            # Improve dark images
            # ------------------------------------------

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            if gray.mean() < 60:

                frame = cv2.convertScaleAbs(
                    frame,
                    alpha=1.4,
                    beta=35
                )

            # ------------------------------------------
            # Face Detection
            # ------------------------------------------

            detections = face_ai.detector.detect(frame)

            recognitions = face_ai.recognizer.recognize(frame)

            self.current_embedding = None
            self.last_face_crop = None

            if recognitions:
                self.current_embedding = recognitions[0].embedding

            if detections is not None:

                for index, det in enumerate(detections):

                    x, y, w, h = det[:4].astype(int)

                    embedding = None
                    name = "Unknown"
                    score = 0.0
                    track_id = 0

                    self.last_face_crop = FaceCropper.crop(
                        frame,
                        det
                    )

                    if index < len(recognitions):

                        result = recognitions[index]

                        embedding = result.embedding

                        track_id = getattr(
                            result,
                            "track_id",
                            0
                        )

                        name, score = (
                            face_ai.recognizer.identify(
                                embedding
                            )
                        )

                        dashboard = self.master

                        if hasattr(
                            dashboard,
                            "set_recognition"
                        ):

                            dashboard.set_recognition(
                                name,
                                score
                            )

                    # -------------------------
                    # Unknown Queue
                    # -------------------------

                    if (
                        name == "Unknown"
                        and embedding is not None
                        and self.last_face_crop is not None
                    ):

                        unknown_queue.add(
                            self.last_face_crop,
                            embedding
                        )

                    color = (
                        (0, 255, 0)
                        if name != "Unknown"
                        else (0, 165, 255)
                    )

                    cv2.rectangle(
                        frame,
                        (x, y),
                        (x + w, y + h),
                        color,
                        2
                    )

                    cv2.putText(
                        frame,
                        f"#{track_id} {name} ({score:.2f})",
                        (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.65,
                        color,
                        2
                    )

            # ------------------------------------------
            # FPS
            # ------------------------------------------

            self.frame_counter += 1

            now = time.time()

            if now - self.last_time >= 1:

                self.fps = self.frame_counter

                dashboard = self.master

                if hasattr(
                    dashboard,
                    "set_fps"
                ):
                    dashboard.set_fps(self.fps)

                self.frame_counter = 0
                self.last_time = now

            cv2.putText(
                frame,
                f"FPS : {self.fps}",
                (15, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.75,
                (0, 255, 255),
                2
            )

            # ------------------------------------------
            # Display
            # ------------------------------------------

            rgb = cv2.cvtColor(
                frame,
                cv2.COLOR_BGR2RGB
            )

            image = Image.fromarray(rgb)

            image = image.resize(
                (800, 450)
            )

            self.camera_image = ctk.CTkImage(
                light_image=image,
                dark_image=image,
                size=(800, 450)
            )

            self.configure(
                image=self.camera_image
            )

        except Exception as error:

            print(error)

        self.after(
            30,
            self.update_frame
        )