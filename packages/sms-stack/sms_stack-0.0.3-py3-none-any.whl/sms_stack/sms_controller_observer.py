from abc import ABC, abstractmethod

class SmsControllerObserver(ABC):

    @abstractmethod
    def handle_final_message_received(self, messages, sender):
        return NotImplemented

    @abstractmethod
    def handle_message_received(self, layer, sender):
        return NotImplemented

    @abstractmethod
    def handle_final_message_sent(self, messages, sender):
        return NotImplemented

    @abstractmethod
    def handle_message_sent(self, layer, sender):
        return NotImplemented