from abc import ABC, abstractmethod

class SmsBroadcaster(ABC):

    @abstractmethod
    def send_sms(self, sms, sender):
        return NotImplemented