from aesDES import *
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import ctypes

root = Tk()

fNormal = ("Garamond", 32, "bold")
fTitle = ("Garamond", 38, "bold")
fButton = ("Century Gothic", 28)
bgColor = '#292826'
fgColor = '#F9D342'

varAlgorithm, varAction, varMode = StringVar(), StringVar(), StringVar()
varKey, varVec = StringVar(), StringVar()
modeRadio = []

aesRadio, desRadio, encRadio, decRadio = Radiobutton(root), Radiobutton(root), Radiobutton(root), Radiobutton(root)
for i in range(5):
    i = Radiobutton(root, variable = varMode, indicatoron = 0, font = fButton, selectcolor = bgColor)
    modeRadio.append(i)
vecEntry = Entry(root, bd = 3, textvariable = varVec, font = fButton, state = DISABLED, show = "*")
keyEntry = Entry(root, bd = 3, textvariable = varKey, font = fButton, show = "*")

def clearData():
    aesRadio.deselect()
    desRadio.deselect()
    encRadio.deselect()
    decRadio.deselect()
    for i in range(5):
        modeRadio[i].deselect()
    keyEntry.delete(0, 'end')
    vecEntry.delete(0, 'end')

def closingVerified():
    request = messagebox.askquestion('Exit Application','Are you sure you want to exit the app?', icon = 'warning')
    if request == 'yes':
       root.destroy()
    return

def vecNeeded():
    if (int(varMode.get())):
        vecEntry.config(state = NORMAL)
    else:
        vecEntry.delete(0, 'end')
        vecEntry.config(state = DISABLED)
    return

def startAction():
    alg, act, mod = varAlgorithm.get(), varAction.get(), varMode.get()
    key, init = varKey.get(), varVec.get()
    if (act == '' or alg == '' or mod == '' or key == ''):
        messagebox.showwarning("Data Incomplete", "You need to choose from every field")
        return
    else:
        if (int(alg)):
            if (len(key) != 8 and key != ''):
                messagebox.showwarning("Key Invalid", "Your key's length must be 8 characters")
                return
        else:
            if (len(key) != 16 and key != ''):
                messagebox.showwarning("Key Invalid", "Your key's length must be 16 characters")
                return
        if (mod != '' and int(mod)):
            if (init == ''):
                messagebox.showwarning("Data Incomplete", "You need to choose from every field")
                return
            if (int(alg)):
                if (len(init) != 8):
                    messagebox.showwarning("Init Vector Invalid", "Your init vector's length must be 8 characters")
                    return
            else:
                if (len(init) != 16):
                    messagebox.showwarning("Init Vector Invalid", "Your init vector's length must be 16 characters")
                    return
    offset, imagePath = openImage()
    if (imagePath == -1): messagebox.showerror("Error", "Image can't load.")
    else:
        if (int(alg)):
            if (act == 'e'): encryptionDES(imagePath, offset, key.encode(), init.encode(), int(mod), act)
            if (act == 'd'): decryptionDES(imagePath, offset, key.encode(), init.encode(), int(mod), act)
        else:
            if (act == 'e'): encryptionAES(imagePath, offset, key.encode(), init.encode(), int(mod), act)
            if (act == 'd'): decryptionAES(imagePath, offset, key.encode(), init.encode(), int(mod), act)
        request = messagebox.askquestion('Operation Completed','Do you want to clear the form?', icon = 'info')
        if request == 'yes':
            clearData()
        return
if __name__ == "__main__":
    root.minsize(width = 840, height = 900)
    root.maxsize(width = 840, height = 900)
    root.configure(bg = bgColor)
    root.title('Image Encryption App')
    root.iconbitmap('Icons/crypto.ico')

    mainMenu = Menu(root)
    mainMenu.add_command(label = "Close", command = quit)
    mainMenu.add_separator()
    mainMenu.add_command(label = "Clear data", command = clearData)
    root.config(menu = mainMenu)

    Label(root, text = "Image Encryption", bg = fgColor, fg = bgColor, font = fTitle).place(x = 95, y = 30, width = 650, height = 60)
    Label(root, text = "Algorithm:", bg = bgColor, fg = fgColor, font = fNormal).place(x = 128, y = 150)
    aesRadio.config(text = "AES", variable = varAlgorithm, value = '0', indicatoron = 0, font = fButton, selectcolor = bgColor)
    aesRadio.place(x = 536, y = 150, width = 100, height = 60)
    desRadio.config(text = "DES", variable = varAlgorithm, value = '1', indicatoron = 0, font = fButton, selectcolor = bgColor)
    desRadio.place(x = 436, y = 150, width = 100, height = 60)

    Label(root, text = "Action:", bg = bgColor, fg = fgColor, font = fNormal).place(x = 128, y = 250)
    encRadio.config(text = "DECRYPT", variable = varAction, value = 'd', indicatoron = 0, font = fButton, selectcolor = bgColor)
    encRadio.place(x = 535, y = 250, width = 180, height = 60)
    decRadio.config(text = "ENCRYPT", variable = varAction, value = 'e', indicatoron = 0, font = fButton, selectcolor = bgColor)
    decRadio.place(x = 355, y = 250, width = 180, height = 60)

    Label(root, text = "Mode:", bg = bgColor, fg = fgColor, font = fNormal).place(x = 128, y = 380)
    modeRadio[0].config(text = "ECB", value = '0', command = vecNeeded)
    modeRadio[0].place(x = 436, y = 350, width = 100, height = 60)
    modeRadio[1].config(text = "CBC", value = '1', command = vecNeeded)
    modeRadio[1].place(x = 536, y = 350, width = 100, height = 60)
    modeRadio[2].config(text = "CFB", value = '2', command = vecNeeded)
    modeRadio[2].place(x = 384, y = 410, width = 100, height = 60)
    modeRadio[3].config(text = "OFB", value = '3', command = vecNeeded)
    modeRadio[3].place(x = 484, y = 410, width = 100, height = 60)
    modeRadio[4].config(text = "CTR", value = '4', command = vecNeeded)
    modeRadio[4].place(x = 584, y = 410, width = 100, height = 60)

    Label(root, text = "Key:", bg = bgColor, fg = fgColor, font = fNormal).place(x = 128, y = 510)
    keyEntry.place(x = 355, y = 510, width = 370)

    Label(root, text = "Init Vec:", bg = bgColor, fg = fgColor, font = fNormal).place(x = 128, y = 610)
    vecEntry.place(x = 355, y = 610, width = 370)

    Button(root, text = "SELECT\nIMAGE", command = startAction, font = fButton).place (x = 345, y = 760)
    ctypes.windll.shcore.SetProcessDpiAwareness(2)
    root.protocol('WM_DELETE_WINDOW', closingVerified)
    root.mainloop()