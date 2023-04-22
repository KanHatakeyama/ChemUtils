# set resource for pyinstaller
# main
from ChemGUI.Notebook import NoteBook
import tkinter as tk

# 解像度をup
import ctypes

try:
    ctypes.windll.shcore.SetProcessDpiAwareness(True)
except:
    pass


root = tk.Tk()
notebook = NoteBook(root)

root.geometry("1000x800")
root.title("ChemGUI 20230422_")
notebook.mainloop()
