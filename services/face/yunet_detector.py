"""
YuNet Face Detector
"""

from pathlib import Path
import cv2


class YuNetDetector:

    def __init__(self):

        model = Path("models/yunet/face_detection_yunet_2023mar.onnx")

        if not model.exists():
            raise FileNotFoundError(
                f"YuNet model not found:\n{model.resolve()}"
            )

        self.detector = cv2.FaceDetectorYN.create(
            str(model),
            "",
            (320, 320),
        )

    def detect(self, frame):

        h, w = frame.shape[:2]

        self.detector.setInputSize((w, h))

        retval, faces = self.detector.detect(frame)

        return faces