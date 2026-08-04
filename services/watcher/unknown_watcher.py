import time


class UnknownWatcher:

    def __init__(self):

        self.first_seen = None
        self.triggered = False

    def update(self, person_name):

        if person_name != "Unknown":

            self.first_seen = None
            self.triggered = False
            return False

        if self.first_seen is None:
            self.first_seen = time.time()

        elapsed = time.time() - self.first_seen

        if elapsed > 3 and not self.triggered:

            self.triggered = True
            return True

        return False

    def reset(self):

        self.first_seen = None
        self.triggered = False


unknown_watcher = UnknownWatcher()