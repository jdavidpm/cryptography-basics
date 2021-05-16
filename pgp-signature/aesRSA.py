from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from rsa import *

def encryptText(data):
    key = get_random_bytes(16)
    cipher = AES.new(key, AES.MODE_EAX)
    cipherText = cipher.encrypt(data)
    keyCipher = encrypt(key, RSA.import_key(open('davidPublic.pem').read()))
    #signature = sign(data, RSA.import_key(open('davidPrivate.pem').read()), "SHA-512")
    with open("encrypted.bin", "wb") as f:
        [f.write(x) for x in (keyCipher, cipher.nonce, cipherText)]
        
def decryptText():
    with open("encrypted.bin", "rb") as f:
        keyCipher, nonce, ciphertext = [f.read(x) for x in (128, 16, -1)]
        key = decrypt(keyCipher, RSA.import_key(open('davidPrivate.pem').read()))
        cipher = AES.new(key, AES.MODE_EAX, nonce)
        data = cipher.decrypt(ciphertext)
        #ver = verify(data, signature, RSA.import_key(open('damianPublic.pem').read()))
        return data
    
if __name__ == "__main__":
    encryptText(b"Hola, mundokkkkkkkkkkkkkkmijnjnuh 24242 \n2")
    print(decryptText().decode())
