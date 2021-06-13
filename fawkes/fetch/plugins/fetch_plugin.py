from abc import ABC, abstractmethod

class FetchPlugin(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def fetch(self):
        pass