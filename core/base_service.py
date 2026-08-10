"""
Base Service
Recognition System v2
"""

from abc import ABC, abstractmethod


class BaseService(ABC):
    """
    Abstract base class for all application services.
    """

    def __init__(self, name: str):
        self.name: str = name
        self.running: bool = False

    @abstractmethod
    def start(self) -> None:
        """
        Start the service.
        """
        ...

    @abstractmethod
    def stop(self) -> None:
        """
        Stop the service.
        """
        ...

    def restart(self) -> None:
        """
        Restart the service safely.
        """
        if self.running:
            self.stop()
        self.start()

    def is_running(self) -> bool:
        """
        Return service running state.
        """
        return self.running

    def status(self) -> dict:
        """
        Return current service status.
        """
        return {
            "name": self.name,
            "running": self.running,
        }

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}"
            f"(name='{self.name}', running={self.running})"
        )