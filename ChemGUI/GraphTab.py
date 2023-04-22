import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from .SaveSettings import SaveSettings
import pandas as pd
from tkinter import messagebox
from openpyxl import load_workbook
from .ChemGraph import export_html

settings = SaveSettings()

graph_setting_list = [
    "SMILES",
    "x",
    "y",
    "color",
]


class GraphTab(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        pass

    def refresh_widgets(self):
        for widget in self.winfo_children():
            widget.destroy()

        self.create_custom_widgets()

    def create_custom_widgets(self):
        label = tk.Label(
            self, text=f'Select SMILES column', font=('Arial', 12))
        label.pack()

        self.combo_dict = {}

        columns = list(self.master.df.columns)
        for c in graph_setting_list:

            label = tk.Label(
                self, text=f'Select {c}', font=('Arial', 12))
            label.pack()

            combo = ttk.Combobox(
                self, values=columns, state='readonly')
            combo.set(columns[0])
            combo.pack()

            self.combo_dict[c] = combo

        self.load_button = tk.Button(
            self, text="Generate graph", command=self.on_button_click_load)
        self.load_button.pack()

    def on_button_click_load(self):
        try:
            self.generate_graph()
            messagebox.showinfo(
                "success", "Graph generated successfully!")

        except Exception as e:
            messagebox.showinfo("error", "Load error"+str(e))

    def generate_graph(self):
        file_path = filedialog.asksaveasfilename(defaultextension='.html')

        if file_path:
            export_html(
                self.master.df,
                self.combo_dict["x"].get(),
                self.combo_dict["y"].get(),
                self.combo_dict["color"].get(),
                self.combo_dict["SMILES"].get(),
                file_path,
            )
