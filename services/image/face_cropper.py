"""
Face Cropper
Recognition System v2
"""

import cv2

from config.settings import Settings
from core.logger.logger import app_logger


class FaceCropper:

    @staticmethod
    def crop(frame, face):

        if frame is None:

            return None

        if face is None:

            return None

        try:

            x, y, w, h = face[:4].astype(int)

        except Exception:

            app_logger.warning(
                "Invalid face coordinates."
            )

            return None

        padding = getattr(
            Settings,
            "FACE_PADDING",
            25
        )

        x1 = max(
            0,
            x - padding
        )

        y1 = max(
            0,
            y - padding
        )

        x2 = min(
            frame.shape[1],
            x + w + padding
        )

        y2 = min(
            frame.shape[0],
            y + h + padding
        )

        if x2 <= x1 or y2 <= y1:

            return None

        face_image = frame[
            y1:y2,
            x1:x2
        ]

        if face_image.size == 0:

            return None

        crop_size = getattr(
            Settings,
            "FACE_CROP_SIZE",
            300
        )

        try:

            face_image = cv2.resize(

                face_image,

                (
                    crop_size,
                    crop_size
                )

            )

        except Exception as e:

            app_logger.exception(e)

            return None

        return face_image