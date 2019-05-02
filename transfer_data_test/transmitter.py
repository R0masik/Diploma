"""Transmitter test"""

import socket
from crypto_test import Encryptor


# sock = socket.socket()
# sock.connect(('localhost', 9090))
# s = 'hello, world!'.encode('utf-8')
# sock.send(s)
#
# data = sock.recv(1024)
# sock.close()
#
# print(data)

class Transmitter:
    def __init__(self, port):
        self.sock = socket.socket()
        self.sock.connect(('localhost', port))

    def send(self, data):
        encryptor = Encryptor()

        enc_data = encryptor.encrypt(data)
        self.sock.send(enc_data)

        resp = self.sock.recv(1024)
        dec_resp = encryptor.decrypt(resp)
        self.sock.close()

        return dec_resp


if __name__ == '__main__':
    my_data = 'Tipo tipo tipo tipo tipo'.encode('utf-8')
    transmitter = Transmitter(9090)
    print(transmitter.send(my_data))
