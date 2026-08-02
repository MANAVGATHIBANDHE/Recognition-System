"""
Base Service
Recognition System
"""

from abc import ABC, abstractmethod


class BaseService(ABC):
    """
    Base class for every service.
    """

    def __init__(self, name: str):
        self.name = name
        self.running = False

    @abstractmethod
    def start(self):
        """
        Start the service.
        """

    @abstractmethod
    def stop(self):
        """
        Stop the service.
        """

    def restart(self):
        self.stop()
        self.start()

    def is_running(self):
        return self.running

    def status(self):
        return {
            "name": self.name,
            "running": self.running
        }