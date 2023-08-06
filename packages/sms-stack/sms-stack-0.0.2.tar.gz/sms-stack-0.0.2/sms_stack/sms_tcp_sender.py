from .sms_tcp import SmsTcp
from .sms_tcp_layer import SmsTcpLayer
from .cipher import AESCipher

class SmsTcpSender(SmsTcp):

    def __init__(self, cipher_mode, cipher_key, controller, broadcast_send):        
        super().__init__(cipher_mode, cipher_key, broadcast_send)
        self._controller = controller


    def create_new_conversation(self, sms, sender):
        key = super().generate_random_key()
        cipher_text = self.cipher_text(sms)
        message_to_send = self.split_message(cipher_text)
        if(message_to_send is None):
            return
        for idx, message in enumerate(message_to_send):
            self.send_message(message, key, idx, idx == len(message_to_send) -1, sender)
        self._controller.handle_final_message_sent(message_to_send, sender)
    
    def send_message(self, text, key, s_begin, is_fin, sender):
        sms_layer = SmsTcpLayer(id=0, key=key, syn= + (not is_fin), ack=0, psh=0, fin=+is_fin, s_begin=s_begin, cipher=self.cipher_mode, check_sum=0, data=text)
        self.send_sms(sms_layer, sender)
        self._controller.handle_message_sent(sms_layer, sender)

    def cipher_text(self, text):
        cipher_text = ""
        if(self.cipher_mode == 0):
            cipher_text = SmsTcp.encode_base_64(text)
        elif (self.cipher_mode == 1):
            aes_text = AESCipher(self.cipher_key).decrypt(str(text))
            cipher_text = SmsTcp.encode_base_64(aes_text)
        else:
            cipher_text = SmsTcp.encode_base_64(text)

        return cipher_text

    def split_message(self, cipher_text):
        sms_len = self.sms_lenght
        return [cipher_text[i:i+sms_len] for i in range(0, len(cipher_text), sms_len)]
        