from abc import ABC, abstractmethod


class DocumentOutputBase(ABC):
    @abstractmethod
    def save(self, content, **kwargs):
        """Saves the given content to the specified output."""
        pass
