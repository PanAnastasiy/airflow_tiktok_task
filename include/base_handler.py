from abc import abstractmethod


class BaseHandler:

    @abstractmethod
    def read(self):
        ...
