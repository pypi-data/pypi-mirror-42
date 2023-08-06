from .sms_tcp_layer_formatter import SmsTcpLayerFormatter

class SmsTcpLayer:

    def __init__(self, sms='', id=None, key=None, syn=None, ack=None, psh=None, fin=None, s_begin=None, cipher=None, check_sum=None, data=""):
        if(sms != ''):
            self._decode_sms(sms)
        elif(id != None, key != None, syn != None, ack != None, psh != None, fin != None, s_begin != None, cipher != None, check_sum != None):
            self.id = id
            self.key = key
            self.syn = syn
            self.ack = ack
            self.psh = psh
            self.fin = fin
            self.s_begin = s_begin
            self.cipher = cipher
            self.check_sum = check_sum
            self.data = data


    def _decode_sms(self, sms):
        try:
            header_sms = SmsTcpLayerFormatter.fill_header_string(SmsTcpLayerFormatter.hex_to_binary(sms[0:14]), 56)
            self.data = sms[14:]
            self.id = int(header_sms[0:1], 2)
            self.key = int(header_sms[1:9], 2)
            self.syn = int(header_sms[9:10], 2)
            self.ack = int(header_sms[10:11], 2)
            self.psh = int(header_sms[11:12], 2)
            self.fin = int(header_sms[12:13], 2)
            self.s_begin = int(header_sms[13:21], 2)
            self.cipher = int(header_sms[21:24], 2)
            self.check_sum = int(header_sms[24:], 2)
        except:
            print("Bad length exception")
        
    
    def enconde_sms(self):
        id_sms = SmsTcpLayerFormatter.fill_header_binary(self.id, 1)
        key_sms = SmsTcpLayerFormatter.fill_header_binary(self.key, 8)
        syn_sms = SmsTcpLayerFormatter.fill_header_binary(self.syn, 1)
        ack_sms = SmsTcpLayerFormatter.fill_header_binary(self.ack, 1)
        psh_sms = SmsTcpLayerFormatter.fill_header_binary(self.psh, 1)
        fin_sms = SmsTcpLayerFormatter.fill_header_binary(self.fin, 1)
        s_begin_sms = SmsTcpLayerFormatter.fill_header_binary(self.s_begin, 8)
        cipher_sms = SmsTcpLayerFormatter.fill_header_binary(self.cipher, 3)
        check_sum_sms = SmsTcpLayerFormatter.fill_header_binary(self.check_sum, 32)

        headers_binary = id_sms + key_sms + syn_sms + ack_sms + psh_sms + fin_sms + s_begin_sms + cipher_sms + check_sum_sms
        headers_hexa = SmsTcpLayerFormatter.fill_header_string(SmsTcpLayerFormatter.binary_to_hex(headers_binary), 14)

        return headers_hexa + self.data

    @staticmethod
    def message_packet_lost(layer, s_begin= None):
        idx = s_begin if s_begin is not None else layer.s_begin
        return SmsTcpLayer(id=layer.id, key=layer.key, syn=0, ack=1, psh=0, fin=0, s_begin=idx, cipher=layer.cipher, check_sum=layer.check_sum, data="")

    @staticmethod
    def message_packet_fin(layer):
        return SmsTcpLayer(id=layer.id, key=layer.key, syn=0, ack=1, psh=0, fin=1, s_begin=layer.s_begin, cipher=layer.cipher, check_sum=layer.check_sum, data="")





