from tkinter.filedialog import asksaveasfilename, askopenfilename
from tkinter import messagebox
import tkinter as tk
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
from rsa import *

root = tk.Tk()
ftTitle = ('Free Mono', 22, 'bold')
ftNormal = ('Free Mono', 21)
ftButton = ('Free Mono', 20)
blColor = '#343838'
baColor = '#005F6B'
bbColor = '#008C9E'
bcColor = '#00B4CC'
bdColor = '#00DFFC'

conVar, autVar = tk.StringVar(), tk.StringVar()
conVar.set(0)
autVar.set(0)
publicKey, privateKey, Message = None, None, None
serviceSelected = None

def placeWindow(window, xRef, yRef):
    x, y = window.winfo_x(), window.winfo_y()
    w, h = window.winfo_width(), window.winfo_height()  
    window.geometry("%dx%d+%d+%d" % (w, h, x + xRef, y + yRef))

def returnRoot(window):
    root.deiconify()
    window.destroy()

def encryptMessage():
    global publicKey
    global privateKey
    global Message
    global serviceSelected
    data = open(Message, 'rb')
    data = data.read()
    key = get_random_bytes(16)
    cipher = AES.new(key, AES.MODE_CBC)
    cipherText = cipher.encrypt(pad(data, AES.block_size))
    keyCipher = encrypt(key, publicKey)
    path = asksaveasfilename(initialfile = 'encryptedMessage.txt', filetypes = (("Text File", "*.txt"), ("All Files", "*.*")), title = "Choose a path.")
    f = open(path, 'wb')
    if serviceSelected:
        signature = sign(data, privateKey, "SHA-512")
        [f.write(x) for x in (signature, keyCipher, cipher.iv, cipherText)]
    else:
        [f.write(x) for x in (keyCipher, cipher.iv, cipherText)]
    messagebox.showinfo("Message encrypted", "Process terminated")

def decryptMessage():
    global publicKey
    global privateKey
    global Message
    f = open(Message, 'rb')
    if serviceSelected:
        signature, keyCipher, iv, ciphertext = [f.read(x) for x in (128, 128, 16, -1)]
    else:
        keyCipher, iv, ciphertext = [f.read(x) for x in (128, 16, -1)]
    try:
        key = decrypt(keyCipher, privateKey)
    except:
        messagebox.showwarning("Message can't be decrypted", "Process terminated\nAES Key modified")
        return
    cipher = AES.new(key, AES.MODE_CBC, iv)
    data = cipher.decrypt(ciphertext)
    print(data)
    if serviceSelected:
        if (verify(data, signature, publicKey)):
            messagebox.showinfo("Message decrypted", "Process terminated\nMessage is verified")
        else:
            messagebox.showinfo("Message decrypted", "Process terminated\nMessage is not verified")
        
    path = asksaveasfilename(initialfile = 'decryptedMessage.txt', filetypes = (("Text File", "*.txt"), ("All Files", "*.*")), title = "Choose a path.")
    f = open(path, 'wb')
    f.write(data)

def signMessage():
    global privateKey
    global Message
    global serviceSelected
    data = open(Message, 'rb')
    data = data.read()
    path = asksaveasfilename(initialfile = 'signMessage.txt', filetypes = (("Text File", "*.txt"), ("All Files", "*.*")), title = "Choose a path.")
    f = open(path, 'wb')
    signature = sign(data, privateKey, "SHA-512")
    [f.write(x) for x in (signature, data)]

def verifyMessage():
    global publicKey
    global Message
    f = open(Message, 'rb')
    chVer = ''
    signature, data = [f.read(x) for x in (128, -1)]
    if (verify(data, signature, publicKey)):
        messagebox.showinfo("Message processed", "Process terminated\nMessage is verified")
    else:
        chVer = 'un'
        messagebox.showinfo("Message processed", "Process terminated\nMessage is not verified")
        
    path = asksaveasfilename(initialfile = chVer + 'verifiedMessage.txt', filetypes = (("Text File", "*.txt"), ("All Files", "*.*")), title = "Choose a path.")
    f = open(path, 'wb')
    f.write(data)

def uploadFile(keyword, buttonChoice):
    global publicKey
    global privateKey
    global Message
    path = askopenfilename(filetypes = (("Key File", "*.pem"), ("Text File", "*.txt"),("All Files","*.*")), title = "Choose " + keyword + ".")
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
            Message = path
    buttonChoice['state'] = 'disabled'

def closeEverything():
    root.destroy()
    
def verifyMessageWindow(window):
    decryptWindow = tk.Toplevel(window)
    window.withdraw()
    decryptWindow.minsize(width = 480, height = 310)
    decryptWindow.maxsize(width = 480, height = 310)
    decryptWindow.title('Verify message')
    placeWindow(decryptWindow, 900, 300)
    decryptWindow.configure(bg = blColor)
    tk.Label(decryptWindow, text = 'Public Key:', font = ftNormal, bg = blColor, fg = bdColor).place(x = 45, y = 30)
    #tk.Label(decryptWindow, text = 'Private Key:', font = ftNormal, bg = blColor, fg = bdColor).place(x = 20, y = 130)
    tk.Label(decryptWindow, text = 'Message:', font = ftNormal, bg = blColor, fg = bdColor).place(x = 122, y = 130)
    publicButton, privateButton, messageButton = tk.Button(decryptWindow), tk.Button(decryptWindow), tk.Button(decryptWindow)
    publicButton.configure(text = 'FILE', font = ftButton, bg = bdColor, fg = blColor, command = lambda: uploadFile('Public Key', publicButton))
    publicButton.place(x = 330, y = 30)
    #privateButton.configure(text = 'FILE', font = ftButton, bg = bdColor, fg = blColor, command = lambda: uploadFile('Private Key', privateButton))
    #privateButton.place(x = 330, y = 130)
    messageButton.configure(text = 'FILE', font = ftButton, bg = bdColor, fg = blColor, command = lambda: uploadFile('Message', messageButton))
    messageButton.place(x = 330, y = 130)
    tk.Button(decryptWindow, text = 'VERIFY', font = ftButton, bg = bdColor, fg = blColor, command = verifyMessage).place(x = 50, y = 220)
    tk.Button(decryptWindow, text = 'RETURN', font = ftButton, bg = bdColor, fg = blColor, command = lambda: returnRoot(decryptWindow)).place(x = 255, y = 220)
    decryptWindow.protocol('WM_DELETE_WINDOW', closeEverything)
    decryptWindow.mainloop()

def signMessageWindow(window):
    decryptWindow = tk.Toplevel(window)
    window.withdraw()
    decryptWindow.minsize(width = 480, height = 310)
    decryptWindow.maxsize(width = 480, height = 310)
    decryptWindow.title('Sign message')
    placeWindow(decryptWindow, 900, 300)
    decryptWindow.configure(bg = blColor)
    #tk.Label(decryptWindow, text = 'Public Key:', font = ftNormal, bg = blColor, fg = bdColor).place(x = 45, y = 30)
    tk.Label(decryptWindow, text = 'Private Key:', font = ftNormal, bg = blColor, fg = bdColor).place(x = 20, y = 30)
    tk.Label(decryptWindow, text = 'Message:', font = ftNormal, bg = blColor, fg = bdColor).place(x = 122, y = 130)
    publicButton, privateButton, messageButton = tk.Button(decryptWindow), tk.Button(decryptWindow), tk.Button(decryptWindow)
    #publicButton.configure(text = 'FILE', font = ftButton, bg = bdColor, fg = blColor, command = lambda: uploadFile('Public Key', publicButton))
    #publicButton.place(x = 330, y = 30)
    privateButton.configure(text = 'FILE', font = ftButton, bg = bdColor, fg = blColor, command = lambda: uploadFile('Private Key', privateButton))
    privateButton.place(x = 330, y = 30)
    messageButton.configure(text = 'FILE', font = ftButton, bg = bdColor, fg = blColor, command = lambda: uploadFile('Message', messageButton))
    messageButton.place(x = 330, y = 130)
    tk.Button(decryptWindow, text = 'SIGN', font = ftButton, bg = bdColor, fg = blColor, command = signMessage).place(x = 50, y = 220)
    tk.Button(decryptWindow, text = 'RETURN', font = ftButton, bg = bdColor, fg = blColor, command = lambda: returnRoot(decryptWindow)).place(x = 255, y = 220)
    decryptWindow.protocol('WM_DELETE_WINDOW', closeEverything)
    decryptWindow.mainloop()
    
def decryptMessageWindow(window):
    decryptWindow = tk.Toplevel(window)
    window.withdraw()
    decryptWindow.minsize(width = 480, height = 410)
    decryptWindow.maxsize(width = 480, height = 410)
    decryptWindow.title('Decrypt message')
    placeWindow(decryptWindow, 900, 300)
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
    tk.Button(decryptWindow, text = 'RETURN', font = ftButton, bg = bdColor, fg = blColor, command = lambda: returnRoot(decryptWindow)).place(x = 255, y = 320)
    decryptWindow.protocol('WM_DELETE_WINDOW', closeEverything)
    decryptWindow.mainloop()
    
def encryptMessageWindow(window):
    encryptWindow = tk.Toplevel(window)
    window.withdraw()
    encryptWindow.minsize(width = 480, height = 410)
    encryptWindow.maxsize(width = 480, height = 410)
    encryptWindow.title('Encrypt message')
    placeWindow(encryptWindow, 900, 300)
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
    tk.Button(encryptWindow, text = 'RETURN', font = ftButton, bg = bdColor, fg = blColor, command = lambda: returnRoot(encryptWindow)).place(x = 255, y = 320)
    encryptWindow.protocol('WM_DELETE_WINDOW', closeEverything)
    encryptWindow.mainloop()
    

def openWindowSelected():
    global serviceSelected
    conPre, autPre = conVar.get(), autVar.get()
    selectedChoice = 0
    if (conPre == '0' and autPre == '0'):
        messagebox.showwarning("Impossible to continue", "At least one option must be selected")
        return
    elif (conPre == '0' and autPre == '1'):
        selectedChoice = 1
    elif (conPre == '1' and autPre == '0'):
        selectedChoice = 2
    elif (conPre == '1' and autPre == '1'):
        selectedChoice = 3
    root.withdraw()
    windowSelected = tk.Toplevel(root)
    windowSelected.minsize(width = 600, height = 600)
    windowSelected.maxsize(width = 600, height = 600)
    windowSelected.configure(bg = baColor)
    windowSelected.title('LOST IN ENCRYPTION')
    placeWindow(windowSelected, 900, 300)
    mainWindow = tk.Frame(windowSelected, width = 600, height = 600, bg = bcColor)
    mainWindow.pack()
    tk.Label(mainWindow, text = 'LOST IN ENCRYPTION', font = ftTitle, fg = blColor, bg = bcColor).place(x = 60, y = 50)
    if (selectedChoice == 2 or selectedChoice == 3):
        serviceSelected = 0 if (selectedChoice == 2) else 1
        tk.Button(mainWindow, text = 'Encrypt Message', font = ftButton, bg = blColor, fg = 'white', command = lambda: encryptMessageWindow(windowSelected)).place(x = 110, y = 170)
        tk.Button(mainWindow, text = 'Decrypt Message', font = ftButton, bg = blColor, fg = 'white', command = lambda: decryptMessageWindow(windowSelected)).place(x = 110, y = 270)
    if (selectedChoice == 1):
        tk.Button(mainWindow, text = 'Sign Message', font = ftButton, bg = blColor, fg = 'white', command = lambda: signMessageWindow(windowSelected)).place(x = 135, y = 170)
        tk.Button(mainWindow, text = 'Verify Message', font = ftButton, bg = blColor, fg = 'white', command = lambda: verifyMessageWindow(windowSelected)).place(x = 110, y = 270)
    tk.Button(mainWindow, text = 'RETURN', font = ftButton, bg = 'green', fg = 'white', command = lambda: returnRoot(windowSelected)).place(x = 130, y = 450)
    tk.Button(mainWindow, text = 'EXIT', font = ftButton, bg = 'red', fg = 'white', command = quit).place(x = 330, y = 450)
    windowSelected.mainloop()
    
if __name__ == "__main__":
    root.minsize(width = 500, height = 450)
    root.maxsize(width = 500, height = 450)
    root.title("LOST IN ENCRYPTION")
    placeWindow(root, 900, 300)
    root.configure(bg = blColor)
    tk.Label(root, text = "LOST IN ENCRYPTION",bg = blColor, fg = bdColor, font = ftTitle).place(x = 15, y = 30)
    tk.Checkbutton(root, text = 'Confidentiality', font = ftButton, bg = blColor, indicatoron = False, selectcolor = bbColor, variable = conVar).place(x = 70, y = 150)
    tk.Checkbutton(root, text = 'Authentication', font = ftButton, bg = blColor, indicatoron = False, selectcolor = bbColor, variable = autVar).place(x = 85, y = 250)
    tk.Button(root, text = "GO", font = ftButton, bg = bdColor, fg = "black", command = openWindowSelected).place(x = 210, y = 370)
    root.wait_visibility(root)
    root.wm_attributes('-alpha', 0.95)
    root.mainloop()
