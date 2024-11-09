from .service_interface import CloudServiceInterface
from .config import Config

class AliService(CloudServiceInterface):
    def __init__(self, name):
        self.name = name

    def show(self):
        return f"{self.name} pwd: {Config.getPwd()}"



