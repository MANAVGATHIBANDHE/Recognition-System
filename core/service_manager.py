"""
Service Manager
Recognition System
"""

from core.logger.logger import logger


class ServiceManager:

    def __init__(self):

        self.services = {}

    def register(self, service):

        self.services[service.name] = service

        logger.info(f"Registered Service -> {service.name}")

    def start(self, name):

        if name in self.services:

            self.services[name].start()

            logger.success(f"{name} Started")

    def stop(self, name):

        if name in self.services:

            self.services[name].stop()

            logger.warning(f"{name} Stopped")

    def restart(self, name):

        if name in self.services:

            self.services[name].restart()

            logger.success(f"{name} Restarted")

    def get(self, name):

        return self.services.get(name)

    def status(self):

        result = {}

        for name, service in self.services.items():

            result[name] = service.status()

        return result