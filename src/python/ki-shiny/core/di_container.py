# core/dependency_injection.py

from services.config_service import ConfigService
from services.my_service import MyService


class DiContainer:
    def __init__(self):
        self.config_service = ConfigService()
        self.my_service = MyService(self.config_service)
