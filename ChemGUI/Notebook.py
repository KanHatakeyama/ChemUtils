import tkinter as tk
import tkinter.ttk as ttk
from .LoadTab import LoadTab
from .DescriptorTab import DescriptorTab
from .GraphTab import GraphTab


class NoteBook(ttk.Notebook):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        # ファイルパスの選択
        self.load_tab = LoadTab(master=self)
        self.add(self.load_tab, text="Load excel", underline=0)

        # 記述子の計算
        self.descriptor_tab = DescriptorTab(master=self)
        self.add(self.descriptor_tab, text="Descriptor", underline=0)

        # グラフ作製
        self.graph_tab = GraphTab(master=self)
        self.add(self.graph_tab, text="Graph & Table", underline=0)
        self.pack(expand=True, fill="both", padx=10, pady=10)

        self.tab(1, state="disabled")
        self.tab(2, state="disabled")

    def unlock_tabs(self):
        self.tab(1, state="normal")
        self.descriptor_tab.refresh_widgets()

        self.tab(2, state="normal")
        self.graph_tab.refresh_widgets()
