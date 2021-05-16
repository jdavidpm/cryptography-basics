#!/usr/bin/python3
from tkinter.filedialog import askopenfilename
import tkinter as tk
import os

def openFile():
	name = askopenfilename(filetypes =(("Text File", "*.txt"),("All Files","*.*")), title = "Choose a file.")
	try:
		with open(name, 'r') as file:
			return name
	except:
		return -1
		
def toenDecrypt(inString):
	xKey = 'K'
	sizeIn = len(inString)
	outString = []
	for i in range(sizeIn):
		outString.append(chr(ord(inString[i]) ^ ord(xKey)))
	return ''.join(outString)

if __name__ == '__main__':
	enDecrypt, yesNo = '', '0'
	while (yesNo == '0'):
		os.system('cls')
		print("Do I want to...\n\ta) Encrypt\n\tb) Decrypt\n")
		enDecrypt = input()
		print("Press [1] to continue or [0] to return: ", '')
		yesNo = input()
	nameFile = openFile()
	if (nameFile == -1):
		print("No existing file")
	else:
		with open(nameFile, 'r') as file:
			string = toenDecrypt(file.read())
		with open(nameFile, 'w') as file:
			file.write(string)