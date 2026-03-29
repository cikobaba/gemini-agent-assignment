import abc
from typing import Any, Dict


class BaseTool(abc.ABC):
    @property
    @abc.abstractmethod
    def name(self) -> str:
        pass

    @abc.abstractmethod
    def execute(self, **kwargs: Any) -> Dict[str, Any]:
        pass

    @abc.abstractmethod
    def get_declaration(self) -> Dict[str, Any]:
        pass