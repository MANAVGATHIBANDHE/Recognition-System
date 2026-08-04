import cv2


class FaceCropper:

    @staticmethod
    def crop(frame, face):

        x, y, w, h = face[:4].astype(int)

        padding = 25

        x1 = max(0, x - padding)
        y1 = max(0, y - padding)

        x2 = min(frame.shape[1], x + w + padding)
        y2 = min(frame.shape[0], y + h + padding)

        face_image = frame[y1:y2, x1:x2]

        return cv2.resize(
            face_image,
            (300, 300)
        )