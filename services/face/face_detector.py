import cv2
import mediapipe as mp


class FaceDetector:

    def __init__(self):

        self.mp_face = mp.solutions.face_detection

        self.detector = self.mp_face.FaceDetection(
            model_selection=1,
            min_detection_confidence=0.5
        )

        self.drawer = mp.solutions.drawing_utils

    def detect(self, frame):

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        result = self.detector.process(rgb)

        if result.detections:

            for detection in result.detections:

                self.drawer.draw_detection(
                    frame,
                    detection
                )

        return frame