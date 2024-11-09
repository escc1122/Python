from abc import ABC, abstractmethod


class CloudServiceInterface(ABC):
    @abstractmethod
    def show(self):
        pass