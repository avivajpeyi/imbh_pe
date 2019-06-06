
from abc import ABC, abstractmethod


class HTMLTemplate(ABC):

    @abstractmethod
    def render(self,) -> str:
        pass

    @abstractmethod
    @property
    def html(self) -> str:
        pass


