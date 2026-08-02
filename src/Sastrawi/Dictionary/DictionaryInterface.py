from abc import ABC, abstractmethod

class DictionaryInterface(ABC):
    """Interface definition of dictionary."""

    @abstractmethod
    def contains(self, word):
        ...
