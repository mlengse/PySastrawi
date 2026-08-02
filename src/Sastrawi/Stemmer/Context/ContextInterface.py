from abc import ABC, abstractmethod

class ContextInterface(ABC):
    """Interface for the stemming context state."""

    @abstractmethod
    def get_original_word(self):
        ...

    @abstractmethod
    def set_current_word(self, word):
        ...

    @abstractmethod
    def get_current_word(self):
        ...

    @abstractmethod
    def get_dictionary(self):
        ...

    @abstractmethod
    def stop_process(self):
        ...

    @abstractmethod
    def process_is_stopped(self):
        ...

    @abstractmethod
    def add_removal(self, removal):
        ...

    @abstractmethod
    def get_removals(self):
        ...
