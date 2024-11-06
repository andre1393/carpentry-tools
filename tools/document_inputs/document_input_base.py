from abc import ABC, abstractmethod


class DocumentInputBase(ABC):
    @abstractmethod
    def read(self, **kwargs):
        """Saves the given content to the specified output."""
        pass
