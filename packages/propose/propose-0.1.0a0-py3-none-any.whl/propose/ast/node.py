from abc import ABC, abstractmethod

class Node(ABC):
    def __repr__(self):
        return self.__str__()

    @abstractmethod
    def __str__(self):
        pass
