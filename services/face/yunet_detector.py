"""
YuNet Face Detector
Recognition System v2
"""

from pathlib import Path

import cv2

from config.paths import MODELS_DIR
from config.settings import Settings
from core.logger.logger import app_logger


class YuNetDetector:

    def __init__(self):

        model = (
            MODELS_DIR /
            "yunet" /
            "face_detection_yunet_2023mar.onnx"
        )

        if not model.exists():

            raise FileNotFoundError(
                f"YuNet model not found:\n{model.resolve()}"
            )

        self.detector = cv2.FaceDetectorYN.create(

            str(model),

            "",

            Settings.DETECTION_SIZE

        )

        app_logger.success(
            "YuNet Detector Loaded"
        )

    # ---------------------------------------------------------

    def detect(self, frame):

        if frame is None:

            return None

        height, width = frame.shape[:2]

        self.detector.setInputSize(
            (width, height)
        )

        try:

            _, faces = self.detector.detect(
                frame
            )

            return faces

        except Exception as e:

            app_logger.exception(e)

            return None