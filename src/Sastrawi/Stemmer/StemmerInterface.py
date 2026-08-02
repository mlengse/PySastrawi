from abc import ABC, abstractmethod

class StemmerInterface(ABC):
    """The stemmer interface."""

    @abstractmethod
    def stem(self, text):
        ...
