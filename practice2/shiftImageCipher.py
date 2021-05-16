from tkinter.filedialog import asksaveasfilename
from tkinter.filedialog import askopenfilename
from PIL import Image
import tkinter as tk
import ntpath
import os
cdMode, imagePath = '', ''

def openImage():
	path = askopenfilename(filetypes = (("BMP Image File", "*.bmp"),("All Files","*.*")), title = "Choose a image.")
	try:
		tmpImg = Image.open(path)
		return [path, tmpImg]
	except:
		return -1

def saveImage(image, imageName):
	path = asksaveasfilename(initialfile = imageName, filetypes = (("BMP Image File", "*.bmp"),("All Files", "*.*")), title = "Save the image.")
	image.save(path, 'bmp')

def imageCipher(image, key):
	rgbMode = image.convert('RGB')
	pixelMap = image.load()
	width, height = image.size

	for w in range(width):
		for h in range(height):
			r, g, b = rgbMode.getpixel((w, h))
			pixelMap[w, h] = ((r + key[0]) % 256, (g + key[1]) % 256, (b + key[2]) % 256)
	saveImage(image, cdMode + '_' + ntpath.basename(imagePath))

def imageDecipher(image, key):
	rgbMode = image.convert('RGB')
	pixelMap = image.load()
	width, height = image.size

	for w in range(width):
		for h in range(height):
			r, g, b = rgbMode.getpixel((w, h))
			pixelMap[w, h] = ((r - key[0]) % 256, (g - key[1]) % 256, (b - key[2]) % 256)
	saveImage(image, cdMode + '_' + ntpath.basename(imagePath))

if __name__ == "__main__":
	yesNo = '0'
	while (yesNo == '0'):
		os.system('cls')
		print("\t\tShift Image Cipher")
		print("Do I want to...\n\tc) Encrypt\n\td) Decrypt\n")
		cdMode = input()
		print("\nSelect key RGB values [r g b]: ", end = '')
		key = [int(i) for i in input().split()]
		print("Press [1] to continue or [0] to return: ", end = '')
		yesNo = input()
	imagePath, oldImage = openImage()
	if (imagePath == -1):
		print("Error: Image can't load.")
	else:
		if (cdMode == 'c'):
			newImage = imageCipher(oldImage, key)
		if (cdMode == 'd'):
			newImage = imageDecipher(oldImage, key)