from tkinter.filedialog import asksaveasfilename, askopenfilename
from Crypto.Cipher import DES
from PIL import Image
import tkinter as tk
import struct
import ntpath
import os
cdMode =  ''
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

def encryptionDES(imagePath, offset, key, initVector, opMode):
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
	saveImage(header + cipherImage, cdMode + '_' + ntpath.basename(imagePath)[:-4] + '_' + ecMode + '.bmp')

def decryptionDES(imagePath, offset, key, initVector, opMode):
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
	saveImage(header + cipherImage, cdMode + '_' + ntpath.basename(imagePath)[:-4] + '_' + ecMode + '.bmp')

if __name__ == "__main__":
	yesNo = '0'
	initVector = '0'
	key = '0'
	while (yesNo == '0'):
		os.system('cls')
		print("\t\tOperation Modes")
		print("Select function \n\te) Encrypt\n\td) Decrypt\n-> ", end='')
		cdMode = input()
		print("\nSelect mode \n\t0) ECB\n\t1) CBC\n\t2) CFB\n\t3) OFB\n\t4) CTR\n-> ", end = '')
		opMode = int(input())
		print('')
		while (len(key) % 8):
			print("Enter key: ", end= '')
			key = input()
		if (opMode):
			while (len(initVector) % 8):
				print("Enter initialization vector: ", end = '')
				initVector = input()
		print("\nPress [1] to continue or [0] to return: ", end = '')
		yesNo = input()
	offset, imagePath = openImage()
	if (imagePath == -1): print("Error: Image can't load.")
	else:
		if (cdMode == 'e'): encryptionDES(imagePath, offset, key.encode(), initVector.encode(), opMode)
		if (cdMode == 'd'): decryptionDES(imagePath, offset, key.encode(), initVector.encode(), opMode)