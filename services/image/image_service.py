import uuid
import cv2
import os


class ImageService:

    def __init__(self):

        os.makedirs(
            "storage/profiles",
            exist_ok=True
        )

    def save_profile(self, image):

        filename = f"{uuid.uuid4()}.png"

        path = os.path.join(
            "storage/profiles",
            filename
        )

        cv2.imwrite(path, image)

        return path


image_service = ImageService()