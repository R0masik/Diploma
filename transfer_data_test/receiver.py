"""Receiver test"""

import socket
from crypto_test import Encryptor


class Receiver:
    def __init__(self, port):
        self.sock = socket.socket()
        self.sock.bind(('localhost', port))

    def listen(self):
        self.sock.listen(1)
        conn, addr = self.sock.accept()
        encryptor = Encryptor()

        while True:
            recv_data = conn.recv(1024)
            if not recv_data:
                break
            dec_data = encryptor.decrypt(recv_data)

            resp_data = encryptor.encrypt(dec_data.decode('utf-8').upper().encode('utf-8'))
            conn.send(resp_data)

        print('Done')
        conn.close()


if __name__ == '__main__':
    receiver = Receiver(9090)
    receiver.listen()
