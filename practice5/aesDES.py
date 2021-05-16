from tkinter.filedialog import asksaveasfilename, askopenfilename
from Crypto.Cipher import DES, AES
from PIL import Image
import tkinter as tk
import struct
import ntpath
import os
blockSize = 8
paddingChar = '0'
nonce = 0

def openImage():
	path = askopenfilename(filetypes = (("BMP Image File", "*.bmp"),("All Files","*.*")), title = "Choose a image.")
	try:
		with open(path, 'rb') as bmpInfo:
			bmpInfo.read(2).decode()
			struct.unpack('I', bmpInfo.read(4))
			struct.unpack('H', bmpInfo.read(2))
			struct.unpack('H', bmpInfo.read(2))
			offset = struct.unpack('I', bmpInfo.read(4))[0]
			return [offset, path]
	except:
		return -1

def saveImage(image, imageName):
	path = asksaveasfilename(initialfile = imageName, filetypes = (("BMP Image File", "*.bmp"),("All Files", "*.*")), title = "Save the image.")
	with open(path, 'wb') as imageFile:
		imageFile.write(image)

def encryptionDES(imagePath, offset, key, initVector, opMode, cdMode):
	imageFile = open(imagePath, 'rb')
	textImage = imageFile.read()
	header = textImage[:offset]
	plainImage = textImage[offset:] + (((blockSize - len(textImage[offset:])) % blockSize) * paddingChar).encode()
	if (opMode == 0):
		suitDES = DES.new(key, DES.MODE_ECB)
		cipherImage = suitDES.encrypt(plainImage)
		ecMode = 'ecb'
	if (opMode == 1):
		suitDES = DES.new(key, DES.MODE_CBC, initVector)
		cipherImage = suitDES.encrypt(plainImage)
		ecMode = 'cbc'
	if (opMode == 2):
		suitDES = DES.new(key, DES.MODE_CFB, initVector)
		cipherImage = suitDES.encrypt(plainImage)
		ecMode = 'cfb'
	if (opMode == 3):
		suitDES = DES.new(key, DES.MODE_OFB, initVector)
		cipherImage = suitDES.encrypt(plainImage)
		ecMode = 'ofb'
	if (opMode == 4):
		suitDES = DES.new(key, DES.MODE_CTR, nonce=b'', initial_value=initVector)
		cipherImage = suitDES.encrypt(plainImage)
		ecMode = 'ctr'
	saveImage(header + cipherImage, ntpath.basename(imagePath)[:-4] + '_des_' + cdMode + '_' + ecMode + '.bmp')

def decryptionDES(imagePath, offset, key, initVector, opMode, cdMode):
	imageFile = open(imagePath, 'rb')
	textImage = imageFile.read()
	header = textImage[:offset]
	plainImage = textImage[offset:] + (((blockSize - len(textImage[offset:])) % blockSize) * paddingChar).encode()
	if (opMode == 0):
		suitDES = DES.new(key, DES.MODE_ECB)
		cipherImage = suitDES.decrypt(plainImage)
		ecMode = 'ecb'
	if (opMode == 1):
		suitDES = DES.new(key, DES.MODE_CBC, initVector)
		cipherImage = suitDES.decrypt(plainImage)
		ecMode = 'cbc'
	if (opMode == 2):
		suitDES = DES.new(key, DES.MODE_CFB, initVector)
		cipherImage = suitDES.decrypt(plainImage)
		ecMode = 'cfb'
	if (opMode == 3):
		suitDES = DES.new(key, DES.MODE_OFB, initVector)
		cipherImage = suitDES.decrypt(plainImage)
		ecMode = 'ofb'
	if (opMode == 4):
		suitDES = DES.new(key, DES.MODE_CTR, nonce=b'', initial_value=initVector)
		cipherImage = suitDES.decrypt(plainImage)
		ecMode = 'ctr'
	saveImage(header + cipherImage, ntpath.basename(imagePath)[:-4] + '_des_' + cdMode + '_' + ecMode + '.bmp')

def encryptionAES(imagePath, offset, key, initVector, opMode, cdMode):
	imageFile = open(imagePath, 'rb')
	textImage = imageFile.read()
	header = textImage[:offset]
	plainImage = textImage[offset:] + (((blockSize - len(textImage[offset:])) % blockSize) * paddingChar).encode()
	if (opMode == 0):
		suitAES = AES.new(key, AES.MODE_ECB)
		cipherImage = suitAES.encrypt(plainImage)
		ecMode = 'ecb'
	if (opMode == 1):
		suitAES = AES.new(key, AES.MODE_CBC, initVector)
		cipherImage = suitAES.encrypt(plainImage)
		ecMode = 'cbc'
	if (opMode == 2):
		suitAES = AES.new(key, AES.MODE_CFB, initVector)
		cipherImage = suitAES.encrypt(plainImage)
		ecMode = 'cfb'
	if (opMode == 3):
		suitAES = AES.new(key, AES.MODE_OFB, initVector)
		cipherImage = suitAES.encrypt(plainImage)
		ecMode = 'ofb'
	if (opMode == 4):
		suitAES = AES.new(key, AES.MODE_CTR, nonce=b'', initial_value=initVector)
		cipherImage = suitAES.encrypt(plainImage)
		ecMode = 'ctr'
	saveImage(header + cipherImage, ntpath.basename(imagePath)[:-4] + '_aes_' + cdMode + '_' + ecMode + '.bmp')

def decryptionAES(imagePath, offset, key, initVector, opMode, cdMode):
	imageFile = open(imagePath, 'rb')
	textImage = imageFile.read()
	header = textImage[:offset]
	plainImage = textImage[offset:] + (((blockSize - len(textImage[offset:])) % blockSize) * paddingChar).encode()
	if (opMode == 0):
		suitAES = AES.new(key, AES.MODE_ECB)
		cipherImage = suitAES.decrypt(plainImage)
		ecMode = 'ecb'
	if (opMode == 1):
		suitAES = AES.new(key, AES.MODE_CBC, initVector)
		cipherImage = suitAES.decrypt(plainImage)
		ecMode = 'cbc'
	if (opMode == 2):
		suitAES = AES.new(key, AES.MODE_CFB, initVector)
		cipherImage = suitAES.decrypt(plainImage)
		ecMode = 'cfb'
	if (opMode == 3):
		suitAES = AES.new(key, AES.MODE_OFB, initVector)
		cipherImage = suitAES.decrypt(plainImage)
		ecMode = 'ofb'
	if (opMode == 4):
		suitAES = AES.new(key, AES.MODE_CTR, nonce=b'', initial_value=initVector)
		cipherImage = suitAES.decrypt(plainImage)
		ecMode = 'ctr'
	saveImage(header + cipherImage, ntpath.basename(imagePath)[:-4] + '_aes_' + cdMode + '_' + ecMode + '.bmp')