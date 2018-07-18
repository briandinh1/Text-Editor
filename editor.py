import sys
import random
from Tkinter import *
import Tkinter, tkFileDialog, tkMessageBox
from ScrolledText import *


class Editor:
    def __init__(self):
        # init main window of GUI
        self.root = Tk()
        self.root.title('Text Editor - Brian Dinh')
        self.root.minsize(width=800, height = 800)
        self.root.pack_propagate(0)
        self.root.option_add('*tearOff', False)
        # init text box (used as the basis of the text editor)
        self.textBox = ScrolledText(self.root, height=100, relief=SUNKEN, undo=1)
        self.textBox.pack(side=TOP, fill=BOTH)
        # init top menu toolbar elements
        self.menu = Menu(self.root, relief=RAISED)
        self.root.config(menu=self.menu)
        self.fileMenu = Menu(self.menu)
        self.fileMenu.add_command(label='New', command=self.newFile, accelerator='Ctrl+N')
        self.fileMenu.add_command(label='Open', command=self.openFile, accelerator='Ctrl+O')
        self.fileMenu.add_command(label='Save', command=self.saveFile, accelerator='Ctrl+S')
        self.fileMenu.add_command(label='Save As', command=self.saveAsFile)
        self.fileMenu.add_separator()
        self.fileMenu.add_command(label='Exit', command=self.root.destroy)
        self.editMenu = Menu(self.menu)
        self.editMenu.add_command(label='Undo', command=self.textBox.edit_undo, accelerator='Ctrl+Z')
        self.editMenu.add_separator()
        self.editMenu.add_command(label='Cut', command=self.cut, accelerator='Ctrl+X')
        self.editMenu.add_command(label='Copy', command=self.copy, accelerator='Ctrl+C')
        self.editMenu.add_command(label='Paste', command=self.paste, accelerator='Ctrl+V')
        self.editMenu.add_separator()
        self.editMenu.add_command(label='Select All', command=self.selectAll, accelerator='Ctrl+A')
        self.menu.add_cascade(label='File', menu=self.fileMenu)
        self.menu.add_cascade(label='Edit', menu=self.editMenu)
        # key binds - missing undo because Tkinter has its own built in
        # don't need keybinds for ctrl x,c,v - os handles it, just use clipboard contents
        self.textBox.bind_all('<Control-n>', self.newFile)
        self.textBox.bind_all('<Control-o>', self.openFile)
        self.textBox.bind_all('<Control-s>', self.saveFile)
        self.textBox.bind_all('<Control-a>', self.selectAll)
        # variables
        self.fileName = ''
        
    def runGUI(self):
        self.root.mainloop()

    def updateTitleBar(self):
        self.root.title('Text Editor - ' + self.fileName)

    def openFile(self, event=None):
        fname = tkFileDialog.askopenfilename()
        if fname: # prevent file opener from overwriting existing
            self.fileName = fname
            contents = self.readFile(self.fileName)
            self.textBox.delete(1.0, END)
            self.textBox.insert(INSERT, contents)
            self.updateTitleBar()

    def readFile(self, fileName):
        f = open(fileName, 'r')
        contents = f.read()
        f.close()
        return contents

    def newFile(self, event=None):
        self.textBox.delete(1.0, END)
        self.fileName = 'New Text Document'
        self.updateTitleBar()

    def saveFile(self, event=None):
        contents = self.textBox.get(1.0, END)
        if self.fileName:
            f = open(self.fileName, 'w')
            f.write(self.textBox.get(1.0, END))
            f.close()
        else:
            self.saveAsFile()

    def saveAsFile(self):
        contents = self.textBox.get(1.0, END)
        fname = tkFileDialog.asksaveasfilename()
        if fname:
            self.fileName = fname
            f = open(self.fileName, 'w')
            f.write(self.textBox.get(1.0, END))
            f.close()
            self.updateTitleBar()

    def selectAll(self, event=None):
        self.textBox.tag_add(SEL, 1.0, END)
        self.textBox.mark_set(INSERT, 1.0)
        self.textBox.see(INSERT)
        return 'break'

    def copy(self, event=None):
        self.textBox.clipboard_clear()
        self.textBox.clipboard_append(self.textBox.get('sel.first', 'sel.last'))

    def cut(self, event=None):
        self.copy()
        self.textBox.delete('sel.first', 'sel.last')
    
    def paste(self, event=None):
        self.textBox.insert(INSERT, self.textBox.selection_get(selection='CLIPBOARD'))

    
        
def main():
    editor = Editor()
    editor.runGUI()
    
if __name__ == "__main__":
    main()
