import time
import numpy as np


class RecognitionCache:

    def __init__(self):

        self.cache = {}

        self.cooldown = 2.0

        self.similarity_threshold = 0.92

    def cosine_similarity(
        self,
        a,
        b
    ):

        return float(np.dot(a, b))

    def get(
        self,
        embedding
    ):

        now = time.time()

        expired = []

        for uid, item in self.cache.items():

            if now - item["time"] > self.cooldown:
                expired.append(uid)

        for uid in expired:
            del self.cache[uid]

        for item in self.cache.values():

            score = self.cosine_similarity(
                embedding,
                item["embedding"]
            )

            if score >= self.similarity_threshold:

                return item["result"]

        return None

    def put(
        self,
        embedding,
        result
    ):

        self.cache[str(time.time())] = {

            "embedding": embedding.copy(),

            "result": result,

            "time": time.time()
        }


recognition_cache = RecognitionCache()