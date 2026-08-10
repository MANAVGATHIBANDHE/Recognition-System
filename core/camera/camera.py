"""
Camera
Recognition System v2
"""

import cv2

from config.settings import Settings
from core.logger.logger import app_logger


class Camera:

    def __init__(self, camera_id: int | None = None):

        self.camera_id = (
            Settings.CAMERA_INDEX
            if camera_id is None
            else camera_id
        )

        self.cap = None

    def open(self) -> bool:
        """
        Open the camera.
        """

        if self.cap is not None and self.cap.isOpened():
            return True

        self.cap = cv2.VideoCapture(self.camera_id)

        if not self.cap.isOpened():

            app_logger.error(
                f"Unable to open camera {self.camera_id}"
            )

            self.cap = None
            return False

        self.cap.set(
            cv2.CAP_PROP_FRAME_WIDTH,
            Settings.CAMERA_WIDTH
        )

        self.cap.set(
            cv2.CAP_PROP_FRAME_HEIGHT,
            Settings.CAMERA_HEIGHT
        )

        self.cap.set(
            cv2.CAP_PROP_FPS,
            Settings.CAMERA_FPS
        )

        app_logger.success(
            f"Camera {self.camera_id} opened successfully."
        )

        return True

    def read(self):
        """
        Read one frame.
        """

        if self.cap is None:

            return False, None

        if not self.cap.isOpened():

            return False, None

        ok, frame = self.cap.read()

        if not ok:

            app_logger.warning(
                "Failed to read camera frame."
            )

            return False, None

        return True, frame

    def is_open(self) -> bool:
        """
        Check whether camera is opened.
        """

        return (
            self.cap is not None
            and
            self.cap.isOpened()
        )

    def release(self) -> None:
        """
        Release camera resources.
        """

        if self.cap is not None:

            self.cap.release()

            self.cap = None

            app_logger.info(
                f"Camera {self.camera_id} released."
            )

    def __del__(self):

        self.release()