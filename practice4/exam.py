from Crypto.Cipher import AES,DES
from Crypto import Random
import struct

iv_AES = Random.new().read(AES.block_size)
iv_DES = Random.get_random_bytes(8)

key_AES = b'abcdefghijklmnop'
key_DES = b'abcdefgh'

aese = AES.new(key_AES,AES.MODE_CFB,iv_AES)#Using Cipher Feedback
aesd = AES.new(key_AES,AES.MODE_CFB,iv_AES)#Using Cipher Feedback
dese = DES.new(key_DES,DES.MODE_ECB) #Using Electronic Cipher Block 
desd = DES.new(key_DES,DES.MODE_ECB) #Using Electronic Cipher Block

blockSize = 8
padding = "0"
offset = 0
with open('./exs.bmp', 'rb') as bmpInfo:
	bmpInfo.read(2).decode()
	struct.unpack('I', bmpInfo.read(4))
	struct.unpack('H', bmpInfo.read(2))
	struct.unpack('H', bmpInfo.read(2))
	offset = struct.unpack('I', bmpInfo.read(4))[0]
	print(offset)
imageFile = open('./exs.bmp', 'rb')
textimage = imageFile.read()
header = textimage[:offset]
plaintext = textimage[offset:] + (((blockSize - len(textimage[offset:])) % blockSize) * padding).encode()

imageFile = open('./nuevo.bmp', 'wb')
imageFile.write(header+dese.encrypt(plaintext))
#print (aesd.decrypt(aese.encrypt(plaintext)))
#print (desd.decrypt(dese.encrypt(plaintext)))