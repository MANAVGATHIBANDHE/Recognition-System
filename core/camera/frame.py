import cv2


class Frame:

    @staticmethod
    def resize(frame, width=640):

        h, w = frame.shape[:2]

        ratio = width / w

        return cv2.resize(
            frame,
            (width, int(h * ratio))
        )