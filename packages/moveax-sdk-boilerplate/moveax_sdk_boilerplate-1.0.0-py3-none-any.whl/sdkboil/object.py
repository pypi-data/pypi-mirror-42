from abc import ABCMeta, abstractmethod


class SDKObject(metaclass=ABCMeta):
    def to_json(self):
        """
        :return: a json representation of the object
        """
        return self.__dict__

    def __getitem__(self, item):
        return getattr(self, item)


class Receivable(SDKObject, metaclass=ABCMeta):
    @staticmethod
    @abstractmethod
    def get_receiving_schema():
        raise NotImplemented

    @classmethod
    def from_json(cls, obj):
        """
        :param obj: a json dictionary
        :return: the object parsed from the json dictionary
        """
        return cls(**obj)


class Sendable(SDKObject, metaclass=ABCMeta):
    @staticmethod
    @abstractmethod
    def get_sending_schema():
        raise NotImplemented
