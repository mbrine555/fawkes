from abc import ABC, abstractmethod

class Connector(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def fetch(self):
        pass