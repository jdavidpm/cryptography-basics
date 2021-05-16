import tkinter as tk
from keySchedule import *

root = tk.Tk()
bgColor = '#222629'
fgColor = '#F2F2F2'
bnColor = '#61892F'

ftTitle = ('Linux Biolinum Keyboard', 22,  'bold')
ftNormal = ('Linux Libertine Initials', 18)
ftButton = ('Free Mono', 20)

keyOriginal = tk.StringVar()
keyNumber =  tk.StringVar()
nthKey = tk.StringVar()

def generateKey():
	kN = keyNumber.get().split('-')
	if (len(kN) > 1):
		tmp = ''
		for i in range(int(kN[0]), int(kN[1]) + 1):
			tmp += (' ' + str(i).zfill(2) + ') ' + getNKey(keyOriginal.get(), i) + ' \n')
		nthKey.set(tmp)
	else:
		nthKey.set(' ' + getNKey(keyOriginal.get(), int(kN[0])) + ' ')

if __name__ == "__main__":
	root.minsize(width = 500, height = 500)
	root.maxsize(width = 850, height = 1400)
	root.title('Key Schedule Generator')
	root.configure(bg = bnColor)
	mainWindow = tk.Frame(root)
	mainWindow.pack(expand = 1)
	mainWindow.configure(bg = bgColor)
	tk.Label(mainWindow, text = 'KEY\nSCHEDULE\nGENERATOR', bg = bgColor, fg = fgColor, font = ftTitle, pady = 10, padx = 10).grid(pady = 10, row = 0, columnspan = 3)
	tk.Label(mainWindow, text = 'KEY: ', bg = bgColor,  font = ftNormal).grid(padx = 5, pady = 10, row = 10, column = 0)
	tk.Entry(mainWindow, textvariable = keyOriginal, bd = 3, font = ftButton, show = '*', width = 8).grid(padx = 5, pady = 10, row = 10, column = 1)
	tk.Label(mainWindow, text = '#K:', bg = bgColor, fg = fgColor, font = ftNormal).grid(padx = 5, pady = 10, row = 11, column = 0)
	tk.Spinbox(mainWindow, textvariable = keyNumber,  from_ = 1, to = 16, font = ftButton, width = 5, wrap = True).grid(padx = 5, pady = 10, row = 11, column = 1)
	tk.Button(mainWindow, text = "Generate", font = ftButton, bg = bnColor, command = generateKey).grid(padx = 5, pady = 10, row = 14, column = 0, columnspan = 3)
	tk.Label(mainWindow, textvariable = nthKey, font = ftButton, bg = bgColor).grid(padx = 6, pady = 10, row = 15, column = 0, columnspan = 3)
	nthKey.set('---->nth Key<----')
	img = tk.Image("photo", file = "keyi.gif")
	root.wait_visibility(root)
	root.wm_attributes('-alpha', 0.85)
	root.tk.call('wm','iconphoto', root._w, img)
	root.mainloop()
