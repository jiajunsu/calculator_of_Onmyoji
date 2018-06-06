# coding:utf-8

import Tkinter as tk
import tkFileDialog
import ttk

from calculator_of_Onmyoji import data_format


class FileFrame(tk.Frame):
    def __init__(self, file_type, master=None, **options):
        tk.Frame.__init__(self, master=master, **options)
        self.file_type = file_type
        self.filename = ""
        file_extension = (("Excel files", "*.xls"),)
        if 'Data' in file_type:
            self.dia_open = lambda: tkFileDialog.askopenfilename(filetypes=
                    file_extension)
        else:
            self.dia_open = lambda: tkFileDialog.asksaveasfilename(filetypes=
                    file_extension)
        self.statusbar = tk.Label(self, text="", bd=1,
                                  relief=tk.SUNKEN, anchor=tk.W, width=80)
        self.statusbar.pack(side=tk.BOTTOM, fill=tk.X)

        self.file_button = tk.Button(self, text=self.file_type,
                                     command=self.get_file)
        self.file_button.pack()
        self.pack()

    def get_file(self):
        self.filename = self.dia_open()
        self.statusbar.config(text=self.file_type + self.filename)


class DataBox(tk.Frame):
    def __init__(self, data, master=None, **options):
        tk.Frame.__init__(self, master=master, **options)
        self.data_chosen = ttk.Combobox(master, width=12,
                                        textvariable=tk.StringVar(),
                                        state='readonly')
        self.data_chosen['values'] = data

        self.value_input = tk.Text(master, height=1, width=12)

        self.data_chosen.pack()
        self.value_input.pack()
        self.pack()


if __name__ == '__main__':
    root = tk.Tk(className=u'calculator')
    root.geometry('800x600')

    data_frm = FileFrame('Data file', master=root)
    result_frm = FileFrame('Output file', master=root)

    mitama_frm = DataBox(data_format.MITAMA_TYPES, master=root)
    prop_frm = DataBox(data_format.MITAMA_PROPS, master=root)

    root.mainloop()
