from tkinter.filedialog import asksaveasfilename, askopenfilename
from tkinter import messagebox
import tkinter as tk
from base64 import b64encode, b64decode
from Crypto.PublicKey import RSA
import rsa

root = tk.Tk()
ftTitle = ('Free Mono', 22, 'bold')
ftNormal = ('Free Mono', 21)
ftButton = ('Free Mono', 20)
blColor = '#343838'
baColor = '#005F6B'
bbColor = '#008C9E'
bcColor = '#00B4CC'
bdColor = '#00DFFC'

publicKey, privateKey, Message = None, None, None

def encryptMessage():
    global publicKey
    global privateKey
    global Message
    encrypted = []
    arrMessage = [Message[i : i + 86] for i in range(0, len(Message), 86)]
    for i in arrMessage:
        encrypted.append(b64encode(rsa.encrypt(i, publicKey)))
    signature = b64encode(rsa.sign(arrMessage[0], privateKey, "SHA-512"))
    path = asksaveasfilename(initialfile = 'encryptedMessage.txt', filetypes = (("TXT File", "*.txt"), ("All Files", "*.*")), title = "Choose a path.")
    f = open(path, 'wb')
    f.write((b''.join(encrypted)) + b'pdrp51' + signature)
    messagebox.showinfo("Message encrypted", "Process terminated")

def decryptMessage():
    global publicKey
    global privateKey
    global Message
    encrypted, signature = Message.split(b'pdrp51')
    arrDecrypted = []
    encrypted = [encrypted[i : i + 172] for i in range(0, len(encrypted), 172)]
    for i in encrypted:
        arrDecrypted.append(rsa.decrypt(b64decode(i), privateKey))
    verify = rsa.verify(arrDecrypted[0], b64decode(signature), publicKey)
    path = asksaveasfilename(initialfile = 'decryptedMessage.txt', filetypes = (("TXT File", "*.txt"), ("All Files", "*.*")), title = "Choose a path.")
    f = open(path, 'wb')
    f.write((''.join([i.decode() for i in arrDecrypted])).encode())
    if (verify):
        messagebox.showinfo("Message decrypted", "Process terminated\nMessage is verified")
    else:
        messagebox.showinfo("Message decrypted", "Process terminated\nMessage is not verified")

def uploadFile(keyword, buttonChoice):
    global publicKey
    global privateKey
    global Message
    path = askopenfilename(filetypes = (("Key File", "*.pem"), ("TXT File", "*.txt"),("All Files","*.*")), title = "Choose " + keyword + ".")
    if (keyword == 'Public Key'):
        try:
            publicKey = RSA.import_key(open(path).read())
        except:
            messagebox.showwarning("Invalid Key", "You need to select a valid key")
            return
    elif (keyword == 'Private Key'):
        try:
            privateKey = RSA.import_key(open(path).read())
        except:
            messagebox.showwarning("Invalid Key", "You need to select a valid key")
            return
    elif (keyword == 'Message'):
        with open(path, 'rb') as f:
            Message = f.read()
    buttonChoice['state'] = 'disabled'

def closeEverything():
    root.destroy()

def returnMain(window):
    root.deiconify()
    window.destroy()
    
def decryptMessageWindow():
	decryptWindow = tk.Toplevel(root)
	root.withdraw()
	decryptWindow.minsize(width = 480, height = 410)
	decryptWindow.maxsize(width = 480, height = 410)
	decryptWindow.title('Decrypt message')
	decryptWindow.configure(bg = blColor)
	tk.Label(decryptWindow, text = 'Public Key:', font = ftNormal, bg = blColor, fg = bdColor).place(x = 45, y = 30)
	tk.Label(decryptWindow, text = 'Private Key:', font = ftNormal, bg = blColor, fg = bdColor).place(x = 20, y = 130)
	tk.Label(decryptWindow, text = 'Message:', font = ftNormal, bg = blColor, fg = bdColor).place(x = 122, y = 230)
	publicButton, privateButton, messageButton = tk.Button(decryptWindow), tk.Button(decryptWindow), tk.Button(decryptWindow)
	publicButton.configure(text = 'FILE', font = ftButton, bg = bdColor, fg = blColor, command = lambda: uploadFile('Public Key', publicButton))
	publicButton.place(x = 330, y = 30)
	privateButton.configure(text = 'FILE', font = ftButton, bg = bdColor, fg = blColor, command = lambda: uploadFile('Private Key', privateButton))
	privateButton.place(x = 330, y = 130)
	messageButton.configure(text = 'FILE', font = ftButton, bg = bdColor, fg = blColor, command = lambda: uploadFile('Message', messageButton))
	messageButton.place(x = 330, y = 230)
	tk.Button(decryptWindow, text = 'DECRYPT', font = ftButton, bg = bdColor, fg = blColor, command = decryptMessage).place(x = 50, y = 320)
	tk.Button(decryptWindow, text = 'RETURN', font = ftButton, bg = bdColor, fg = blColor, command = lambda: returnMain(decryptWindow)).place(x = 255, y = 320)
	decryptWindow.protocol('WM_DELETE_WINDOW', closeEverything)
	decryptWindow.mainloop()
    
def encryptMessageWindow():
	encryptWindow = tk.Toplevel(root)
	root.withdraw()
	encryptWindow.minsize(width = 480, height = 410)
	encryptWindow.maxsize(width = 480, height = 410)
	encryptWindow.title('Encrypt message')
	encryptWindow.configure(bg = blColor)
	tk.Label(encryptWindow, text = 'Public Key:', font = ftNormal, bg = blColor, fg = bdColor).place(x = 45, y = 30)
	tk.Label(encryptWindow, text = 'Private Key:', font = ftNormal, bg = blColor, fg = bdColor).place(x = 20, y = 130)
	tk.Label(encryptWindow, text = 'Message:', font = ftNormal, bg = blColor, fg = bdColor).place(x = 122, y = 230)
	publicButton, privateButton, messageButton = tk.Button(encryptWindow), tk.Button(encryptWindow), tk.Button(encryptWindow)
	publicButton.configure(text = 'FILE', font = ftButton, bg = bdColor, fg = blColor, command = lambda: uploadFile('Public Key', publicButton))
	publicButton.place(x = 330, y = 30)
	privateButton.configure(text = 'FILE', font = ftButton, bg = bdColor, fg = blColor, command = lambda: uploadFile('Private Key', privateButton))
	privateButton.place(x = 330, y = 130)
	messageButton.configure(text = 'FILE', font = ftButton, bg = bdColor, fg = blColor, command = lambda: uploadFile('Message', messageButton))
	messageButton.place(x = 330, y = 230)
	tk.Button(encryptWindow, text = 'ENCRYPT', font = ftButton, bg = bdColor, fg = blColor, command = encryptMessage).place(x = 50, y = 320)
	tk.Button(encryptWindow, text = 'RETURN', font = ftButton, bg = bdColor, fg = blColor, command = lambda: returnMain(encryptWindow)).place(x = 255, y = 320)
	encryptWindow.protocol('WM_DELETE_WINDOW', closeEverything)
	encryptWindow.mainloop()
	
def generateKeys():
    path = asksaveasfilename(filetypes = (("TXT File", "*.txt"), ("All Files", "*.*")), title = "Choose a path.")
    try:
        rsa.keysGenerator(path[:-4])
    except:
        print('Keys couldn\'t generate')

if __name__ == '__main__':
	root.minsize(width = 600, height = 600)
	root.maxsize(width = 600, height = 600)
	root.configure(bg = baColor)
	root.title('MEMORIES OF MESSAGES')
	mainWindow = tk.Frame(root, width = 600, height = 600, bg = bcColor)
	mainWindow.pack()
	tk.Label(mainWindow, text = 'Memories of Messages', font = ftTitle, fg = blColor, bg = bcColor).place(x = 40, y = 50)
	tk.Button(mainWindow, text = 'Generate Keys', font = ftButton, bg = blColor, fg = 'white', command = generateKeys).place(x = 135, y = 170)
	tk.Button(mainWindow, text = 'Encrypt Message', font = ftButton, bg = blColor, fg = 'white', command = encryptMessageWindow).place(x = 110, y = 270)
	tk.Button(mainWindow, text = 'Decrypt Message', font = ftButton, bg = blColor, fg = 'white', command = decryptMessageWindow).place(x = 110, y = 370)
	tk.Button(mainWindow, text = 'EXIT', font = ftButton, bg = 'red', fg = 'white', command = quit).place(x = 230, y = 500)
	root.wait_visibility(root)
	root.wm_attributes('-alpha', 0.85)
	root.mainloop()
