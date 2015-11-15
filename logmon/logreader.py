from abc import ABCMeta, abstractmethod


class LogReader(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(*args, **kwargs):
        pass

    @abstractmethod
    def attach(self):
        pass

    @abstractmethod
    def detach(self):
        pass

    @abstractmethod
    def read(self):
        pass


