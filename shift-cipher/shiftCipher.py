#!/usr/bin/python3
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import asksaveasfile
import tkinter as tk
import ntpath
import os

def openFile():
	name = askopenfilename(filetypes =(("Text File", "*.txt"),("All Files","*.*")), title = "Choose a file.")
	try:
		with open(name, 'rb') as file:
			return name
	except:
		return -1

def fileSave(outString, fileName):
	dirName = asksaveasfile(mode = 'a', defaultextension = ".txt", initialfile = fileName, filetypes =(("Text File", "*.txt"),("All Files","*.*")), title = "Save file.")
	f = open(dirName.name, 'w+', encoding = "utf-8")
	f.write(outString)

def shiftCipher(plainText, nShift):
	sizeIn = len(plainText)
	cipherText = []
	for i in range(sizeIn):
		cipherText.append(chr(ord(plainText[i]) + (nShift % 26)))
	return ''.join(cipherText)

def shiftDecipher(cipherText, nShift):
	cipherText = cipherText.decode('utf-8')
	sizeIn = len(cipherText)
	plainText = []
	for i in range(sizeIn):
		plainText.append(chr(ord(cipherText[i]) - nShift % 26))
	return ''.join(plainText)

if __name__ == '__main__':
	enDecrypt, yesNo = '', '0'
	nShift = 0
	while (yesNo == '0'):
		os.system('cls')
		print("\t\tShift Cipher")
		print("Do I want to...\n\tc) Encrypt\n\td) Decrypt\n")
		enDecrypt = input()
		print("\nHow many shifts? ")
		nShift = int(input())
		print("Press [1] to continue or [0] to return: ", '')
		yesNo = input()
	dirFile = openFile()
	if (dirFile == -1):
		print("No existing file")
	else:
		if (enDecrypt == 'c'):
			with open(dirFile, 'r') as file:		
				string = shiftCipher(file.read(), nShift)
		if (enDecrypt == 'd'):	
			with open(dirFile, 'rb') as file:		
				string = shiftDecipher(file.read(), nShift)
		try:
			fileSave(string, enDecrypt + ntpath.basename(dirFile))
		except:
			print("File not saved.")