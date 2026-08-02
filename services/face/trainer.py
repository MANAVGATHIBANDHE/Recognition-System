from core.base_service import BaseService
from core.logger.logger import app_logger


class FaceTrainer(BaseService):

    def __init__(self):
        super().__init__("face_trainer")

    def start(self):
        app_logger.info("Face Trainer Running")

    def stop(self):
        app_logger.info("Face Trainer Stopped")