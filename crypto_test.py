"""Crypto test"""

from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES, PKCS1_OAEP

PRIVATE_KEY_FILEPATH = '/Users/r0masik/PycharmProjects/Diploma/private.pem'
PUBLIC_KEY_FILEPATH = '/Users/r0masik/PycharmProjects/Diploma/public.pem'
ENCRYPTED_DATA_FILEPATH = '/Users/r0masik/PycharmProjects/Diploma/encrypted_data.bin'


class Encryptor:
    def __init__(self):
        self.private_key_file = PRIVATE_KEY_FILEPATH
        self.public_key_file = PUBLIC_KEY_FILEPATH

    def gen_keys(self):
        key = RSA.generate(2048)

        private_key = key.export_key()
        with open(self.private_key_file, 'wb') as file:
            file.write(private_key)

        public_key = key.publickey().export_key()
        with open(self.public_key_file, 'wb') as file:
            file.write(public_key)

    def encrypt(self, decrypted_data):
        # initialization RSA public key and session key
        public_key = RSA.import_key(open(self.public_key_file).read())
        session_key = get_random_bytes(16)

        # encrypting session key with RSA
        cipher_rsa = PKCS1_OAEP.new(public_key)
        enc_session_key = cipher_rsa.encrypt(session_key)

        # encrypting data with AES
        cipher_aes = AES.new(session_key, AES.MODE_EAX)
        ciphertext, tag = cipher_aes.encrypt_and_digest(decrypted_data)

        encrypted_data = b''.join((enc_session_key, cipher_aes.nonce, tag, ciphertext))
        return encrypted_data

        # file_out = open(ENCRYPTED_DATA_FILEPATH, 'wb')
        # [file_out.write(x) for x in (enc_session_key, cipher_aes.nonce, tag, ciphertext)]

    def decrypt(self, encrypted_data):
        def deserialize(data_bytes):
            deserialized = []
            for n in (private_key.size_in_bytes(), 16, 16, None):
                deserialized.append(data_bytes[:n])
                data_bytes = data_bytes[n:]
            return deserialized

        private_key = RSA.import_key(open(self.private_key_file).read())
        enc_session_key, nonce, tag, ciphertext = deserialize(encrypted_data)

        cipher_rsa = PKCS1_OAEP.new(private_key)
        session_key = cipher_rsa.decrypt(enc_session_key)

        cipher_aes = AES.new(session_key, AES.MODE_EAX, nonce)
        decrypted_data = cipher_aes.decrypt_and_verify(ciphertext, tag)

        return decrypted_data

        # file_in = open(encrypted_data_file, 'rb')
        # enc_session_key, nonce, tag, ciphertext = [file_in.read(x) for x in (private_key.size_in_bytes(), 16, 16, -1)]


if __name__ == '__main__':
    my_data = 'Tipotipotipotipotipo'.encode('utf-8')

    encryptor = Encryptor()
    enc_data = encryptor.encrypt(my_data)
    data = encryptor.decrypt(enc_data)
    print(data)
