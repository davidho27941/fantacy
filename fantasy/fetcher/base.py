from abc import (
    ABC,
    abstractmethod,
)

class BaseFetcher(ABC):
    @abstractmethod
    def fetch(self,
        sid: str,
        year: str,
        month: str,
        date: str,
    ):
        raise NotImplementedError
    
    @abstractmethod
    def transform(self):
        raise NotImplementedError
