from .sms_tcp_receiver import SmsTcpReceiver
from .sms_tcp_sender import SmsTcpSender
from .sms_tcp import SmsTcp
from .cipher import AESCipher

class SmsTcpController:

    def __init__(self, observer, broadcaster_send, cipher_mode=0, cipher_key=""):
        self.cipher_mode = cipher_mode
        self.cipher_key = cipher_key
        self._observer = observer
        self._receiver = SmsTcpReceiver(cipher_mode, cipher_key, self, broadcaster_send)
        self._sender = SmsTcpSender(cipher_mode, cipher_key, self, broadcaster_send)

    def handle_final_message_received(self, messages, sender):
        self._observer.handle_final_message_received(messages, sender)

    def handle_message_received(self, layer, sender):
        self._observer.handle_message_received(layer, sender)

    def handle_final_message_sent(self, messages, sender):
        self.handle_final_message_sent(messages, sender)

    def handle_message_sent(self, layer, sender):
        self.handle_message_sent

    def send_message(self, sms, sender):
        self._sender.create_new_conversation(sms, sender)

    def receive_message(self, sms, receiver):
        self._receiver.add_new_message(sms, receiver)

    
    def process_message(self, message):
        final_messge = ''.join(message)
        try:
            if(self.cipher_mode == 0):
                return SmsTcp.decode_base_64(final_messge)
            elif(self.cipher_mode == 1):
                aes_cypher = AESCipher()
                clear_text = aes_cypher.decrypt_message(self.cipher_key, final_messge)
                return clear_text
            else:
                return ""
        except Exception as e:
            print(e)
            return ""
