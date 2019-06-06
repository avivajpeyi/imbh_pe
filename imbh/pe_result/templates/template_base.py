from abc import ABC, abstractmethod


class HTMLTemplate(ABC):
    @abstractmethod
    def render(self,) -> str:
        pass

    @property
    @abstractmethod
    def html(self) -> str:
        pass
