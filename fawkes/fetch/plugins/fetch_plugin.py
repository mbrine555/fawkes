from abc import ABC, abstractmethod

class FetchPlugin(ABC):
    plugins = {}
    
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.plugins[cls._platform] = cls

    @abstractmethod
    def fetch(self):
        pass