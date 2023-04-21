from abc import abstractmethod, ABC


class AbstractSession(ABC):

    @abstractmethod
    def get_transport(self):
        pass
