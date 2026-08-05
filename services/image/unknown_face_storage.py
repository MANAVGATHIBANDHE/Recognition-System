"""
Unknown Face Storage
"""

from pathlib import Path
import uuid

import cv2


class UnknownFaceStorage:

    def __init__(self):

        self.directory = Path("storage/unknown_faces")

        self.directory.mkdir(
            parents=True,
            exist_ok=True
        )

    def save(self, image):

        filename = f"{uuid.uuid4()}.png"

        path = self.directory / filename

        cv2.imwrite(
            str(path),
            image
        )

        return str(path)

    def delete(self, path):

        file = Path(path)

        if file.exists():
            file.unlink()


unknown_face_storage = UnknownFaceStorage()