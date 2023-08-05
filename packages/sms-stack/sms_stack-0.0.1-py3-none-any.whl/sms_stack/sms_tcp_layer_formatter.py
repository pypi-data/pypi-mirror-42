import binascii

class SmsTcpLayerFormatter:

    @staticmethod
    def hex_to_binary(hex):
        return bin(int(hex, 16))[2:]
    
    @staticmethod
    def binary_to_hex(bin):
        return hex(int(bin, 2))[2:]
    
    @staticmethod
    def dec_to_binary(dec):
        return "{0:b}".format(dec)

    @staticmethod
    def fill_header_string(header, req_size):
        return header.zfill(req_size)

    @staticmethod
    def fill_header_binary(header, req_size):
        header_to_string = SmsTcpLayerFormatter.dec_to_binary(header)
        return header_to_string.zfill(req_size)