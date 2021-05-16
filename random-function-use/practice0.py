#!/usr/bin/python3
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import asksaveasfile
from cryptography.fernet import Fernet
import tkinter as tk
import os

def openFile(typeFile):
	name = askopenfilename(filetypes =(("Text File", "*.txt"),("All Files","*.*")), title = "Choose " + typeFile)
	try:
		with open(name, 'r') as file:
			return name
	except:
		return -1

def fileSave(outString, typeFile):
	f = asksaveasfile(mode='w', defaultextension=".txt", title = "Save " + typeFile)
	if f is None:
		return
	f.write(outString)
	f.close()
		
def toCipher(plainText):
	key = Fernet.generate_key()
	cipherSuite = Fernet(key)
	cipherText = cipherSuite.encrypt(plainText.encode())
	fileSave(key.decode(), "the key.")
	return (cipherText.decode())

def toDecipher(cipherText, key):
	cipherSuite = Fernet(key.encode())
	plainText = cipherSuite.decrypt(cipherText.encode())
	return (plainText.decode())


if __name__ == '__main__':
	enDecrypt, yesNo = '', '0'
	while (yesNo == '0'):
		os.system('cls')
		print("Do I want to...\n\ta) Encrypt\n\tb) Decrypt\n")
		enDecrypt = input()
		print("Press [1] to continue or [0] to return: ", '')
		yesNo = input()
	nameFile = openFile("a file.")
	if (nameFile == -1):
		print("No existing file")
	else:
		with open(nameFile, 'r') as file:
			if (enDecrypt == 'a'):			
				string = toCipher(file.read())
				fileSave(string, " the encrypted file")
			if (enDecrypt == 'b'):
				dirKey = openFile("the key.")
				with open(dirKey, 'r') as keyFile:
					string = toDecipher(file.read(), keyFile.read())
				fileSave(string, " the decrypted file")