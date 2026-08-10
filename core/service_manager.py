"""
Service Manager
Recognition System v2
"""

from core.logger.logger import logger


class ServiceManager:

    def __init__(self):

        self.services = {}

    def register(self, service) -> None:
        """
        Register a service.
        """

        if service.name in self.services:

            logger.warning(
                f"Service '{service.name}' already registered."
            )

            return

        self.services[service.name] = service

        logger.info(
            f"Registered Service -> {service.name}"
        )

    def start(self, name: str) -> None:
        """
        Start a service.
        """

        service = self.services.get(name)

        if service is None:

            logger.error(
                f"Service '{name}' not found."
            )

            return

        try:

            service.start()

            logger.success(
                f"{name} Started"
            )

        except Exception as e:

            logger.exception(e)

    def stop(self, name: str) -> None:
        """
        Stop a service.
        """

        service = self.services.get(name)

        if service is None:

            logger.error(
                f"Service '{name}' not found."
            )

            return

        try:

            service.stop()

            logger.warning(
                f"{name} Stopped"
            )

        except Exception as e:

            logger.exception(e)

    def restart(self, name: str) -> None:
        """
        Restart a service.
        """

        service = self.services.get(name)

        if service is None:

            logger.error(
                f"Service '{name}' not found."
            )

            return

        try:

            service.restart()

            logger.success(
                f"{name} Restarted"
            )

        except Exception as e:

            logger.exception(e)

    def start_all(self) -> None:
        """
        Start all registered services.
        """

        for name in self.services:

            self.start(name)

    def stop_all(self) -> None:
        """
        Stop all registered services.
        """

        for name in list(self.services.keys())[::-1]:

            self.stop(name)

    def get(self, name: str):
        """
        Return a registered service.
        """

        return self.services.get(name)

    def status(self) -> dict:
        """
        Return status of all services.
        """

        return {

            name: service.status()

            for name, service in self.services.items()

        }

    def count(self) -> int:
        """
        Total registered services.
        """

        return len(self.services)

    def list_services(self) -> list[str]:
        """
        Return all registered service names.
        """

        return list(self.services.keys())