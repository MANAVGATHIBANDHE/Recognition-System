"""
Image Service
Recognition System v2
"""

from __future__ import annotations

import uuid
from datetime import datetime
from pathlib import Path

import cv2

from config.paths import PROFILES_DIR
from core.logger.logger import app_logger


class ImageService:

    def __init__(self):

        PROFILES_DIR.mkdir(
            parents=True,
            exist_ok=True
        )

    # ==========================================================
    # SAVE PROFILE IMAGE
    # ==========================================================

    def save_profile(self, image):

        if image is None:

            app_logger.warning(
                "Cannot save empty image."
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

        path = PROFILES_DIR / filename

        success = cv2.imwrite(
            str(path),
            image
        )

        if not success:

            app_logger.error(
                "Failed to save profile image."
            )

            return None

        app_logger.info(
            f"Profile Image Saved -> {filename}"
        )

        return str(path)

    # ==========================================================
    # DELETE PROFILE IMAGE
    # ==========================================================

    def delete_profile(self, image_path):

        if not image_path:
            return

        path = Path(image_path)

        if path.exists():

            path.unlink()

            app_logger.info(
                f"Deleted Profile Image -> {path.name}"
            )


image_service = ImageService()