"""
Unknown Face Storage
Recognition System v2
"""

from __future__ import annotations

import uuid
from datetime import datetime
from pathlib import Path

import cv2

from config.paths import FILES_DIR
from core.logger.logger import app_logger


class UnknownFaceStorage:

    def __init__(self):

        self.directory = FILES_DIR / "unknown_faces"

        self.directory.mkdir(
            parents=True,
            exist_ok=True
        )

    # ==========================================================
    # SAVE UNKNOWN FACE
    # ==========================================================

    def save(self, image):

        if image is None:

            app_logger.warning(
                "Unknown face image is empty."
            )

            return None

        filename = (
            datetime.now().strftime(
                "%Y%m%d_%H%M%S"
            )
            + "_"
            + str(uuid.uuid4())[:8]
            + ".png"
        )

        path = self.directory / filename

        success = cv2.imwrite(
            str(path),
            image
        )

        if not success:

            app_logger.error(
                "Failed to save unknown face."
            )

            return None

        app_logger.info(
            f"Unknown Face Saved -> {filename}"
        )

        return str(path)

    # ==========================================================
    # DELETE UNKNOWN FACE
    # ==========================================================

    def delete(self, image_path):

        if not image_path:
            return

        file = Path(image_path)

        if file.exists():

            file.unlink()

            app_logger.info(
                f"Deleted Unknown Face -> {file.name}"
            )

    # ==========================================================
    # CLEANUP
    # ==========================================================

    def clear(self):

        count = 0

        for file in self.directory.glob("*.png"):

            file.unlink()

            count += 1

        app_logger.info(
            f"Removed {count} unknown face images."
        )


unknown_face_storage = UnknownFaceStorage()