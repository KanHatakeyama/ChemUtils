import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from .SaveSettings import SaveSettings
import pandas as pd
from tkinter import messagebox


from .calculators.Autodescriptor import (
    RDKitDescriptors,
    Fingerprint,
    GroupContMethod,
    AutoDescriptor,
)
from .calculators.StructureFactor import StructureFactor


settings = SaveSettings()


descriptor_algorithm_dict = {
    "rdkit": RDKitDescriptors(),
    "AvalonFP": Fingerprint(),
    # "mordred2d": MordredDescriptor(),
    "GroupContribution": GroupContMethod(),
    "3D structure factor": StructureFactor(),
}


class DescriptorTab(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        label = tk.Label(self, text=f"Select Descriptors", font=("Arial", 12))
        label.pack()

        # リストボックスを作成する
        self.listbox = tk.Listbox(self, selectmode=tk.MULTIPLE)
        self.listbox.pack(pady=10)

        items = list(descriptor_algorithm_dict.keys())
        for item in items:
            self.listbox.insert(tk.END, item)

    def refresh_widgets(self):
        for widget in self.winfo_children():
            widget.destroy()

        self.create_widgets()
        self.create_custom_widgets()

    def create_custom_widgets(self):
        label = tk.Label(self, text=f"Select SMILES column", font=("Arial", 12))
        label.pack()

        columns = list(self.master.df.columns)
        # smiles column selection
        self.combo = ttk.Combobox(self, values=columns, state="readonly")
        self.combo.set(columns[0])
        self.combo.pack()

        self.load_button = tk.Button(
            self, text="Process!", command=self.on_button_click_load
        )
        self.load_button.pack()

    def on_button_click_load(self):
        try:
            self.calculate_descriptors()
            messagebox.showinfo("success", "Descriptor calculated successfully!")

        except Exception as e:
            messagebox.showinfo("error", "Load error" + str(e))

    def calculate_descriptors(self):
        selected_items = self.listbox.curselection()

        descriptor_algorithms = []
        for i in selected_items:
            descriptor_algorithms.append(descriptor_algorithm_dict[self.listbox.get(i)])
            print(self.listbox.get(i))

        print("algorithms", descriptor_algorithms)
        calculator = AutoDescriptor(calculators=descriptor_algorithms)
        smiles_list = list(self.master.df[self.combo.get()].values)

        # replace repeat units
        smiles_list = [smiles.replace("[*]", "[H]") for smiles in smiles_list]
        smiles_list = [smiles.replace("*", "[H]") for smiles in smiles_list]

        desc_df = calculator(smiles_list)
        self.integ_df = pd.concat([self.master.df, desc_df], axis=1)

        # 重複する列名を削除
        self.integ_df = self.integ_df.loc[:, ~self.integ_df.columns.duplicated()]

        self.save_file()

    def save_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".xlsx")

        if file_path:
            self.integ_df.to_excel(file_path, index=False)
