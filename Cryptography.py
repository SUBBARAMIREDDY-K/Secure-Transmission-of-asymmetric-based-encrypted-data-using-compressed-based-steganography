from rsa_python import rsa
class Cryptography:
    def __init__(self, key_size):
        self.key_size = key_size
        self.key_pair = rsa.generate_key_pair(self.key_size)
        self.public_key, self.private_key = self.key_pair["public"], self.key_pair["private"]
    def encrypt(self, message):
        return rsa.encrypt(message, self.public_key, self.key_pair["modulus"]), self.key_pair["modulus"]
    def decrypt(self, message):
        return rsa.decrypt(message, self.private_key,self.key_pair["modulus"])
    def customDecrypt(self,message,key,n):
        return rsa.decrypt(message, key, n)
    def get_public_key(self):
        return self.public_key
    def get_private_key(self):
        return self.private_key
    def get_key_size(self):
        return self.key_size