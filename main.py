# set resource for pyinstaller
# main
from ChemGUI.Notebook import NoteBook
import tkinter as tk


root = tk.Tk()
notebook = NoteBook(root)

root.geometry("1000x800")
root.title("ChemGUI 20230422_")
notebook.mainloop()
