import cv2

from services.face.recognizer import FaceRecognizer
from services.face.face_database import face_database


class FaceTrainer:

    def __init__(self):

        self.recognizer = FaceRecognizer()

    def start(self):

        print("Face Trainer Running")

    def register(self, frame, name):

        print("Trainer.register() called")

        faces = self.recognizer.recognize(frame)

        print("Faces Found:", len(faces))

        if len(faces) == 0:
            print("No face detected")
            return False

        embedding = faces[0].embedding

        import os
        import uuid

        os.makedirs("data/faces", exist_ok=True)

        filename = f"{uuid.uuid4()}.jpg"

        path = os.path.join(
            "data/faces",
            filename
        )

        cv2.imwrite(path, frame)

        print("Embedding shape:", embedding.shape)

        face_database.add_face(
            name,
            path,
            embedding
        )

        print(f"{name} Registered Successfully")

        return True


face_trainer = FaceTrainer()