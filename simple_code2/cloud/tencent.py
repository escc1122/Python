from .config import Config
from .service_interface import CloudServiceInterface

__all__ = ["TencentService"]

def _private_method():
    print("no")

class TencentService(CloudServiceInterface):
    def __init__(self, name):
        self.name = name

    def show(self):
        return f"{self.name} pwd: {Config.getPwd()}"
