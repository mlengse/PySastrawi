from abc import ABC, abstractmethod

class RemovalInterface(ABC):
    """Interface for an affix removal record."""

    @abstractmethod
    def get_visitor(self):
        ...

    @abstractmethod
    def get_subject(self):
        ...

    @abstractmethod
    def get_result(self):
        ...

    @abstractmethod
    def get_removed_part(self):
        ...

    @abstractmethod
    def get_affix_type(self):
        ...
