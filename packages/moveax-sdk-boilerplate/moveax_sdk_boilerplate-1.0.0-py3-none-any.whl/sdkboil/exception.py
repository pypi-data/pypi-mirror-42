from abc import ABCMeta, abstractmethod


class SDKException(Exception, metaclass=ABCMeta):
    pass


class SDKResponseException(SDKException, metaclass=ABCMeta):
    @staticmethod
    @abstractmethod
    def get_message(request, response):
        raise NotImplemented

    def __init__(self, request, response):
        super().__init__(self.__class__.get_message(request, response))


class ParallelizerException(SDKException):
    def __init__(self, summary, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.summary = summary


class SequentializerException(SDKException):
    def __init__(self, summary, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.summary = summary
