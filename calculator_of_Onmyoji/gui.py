# coding:utf-8

import Tkinter as tk
import tkFileDialog


class FileFrame(tk.Frame):
    def __init__(self, file_type, master=None, **options):
        tk.Frame.__init__(self, master=master, **options)
        self.file_type = file_type
        self.filename = ""
        self.dialog_open = tkFileDialog.Open(self.master,
                                             filetypes=(("Excel files",
                                                         "*.xls"),))
        self.statusbar = tk.Label(self, text="", bd=1,
                                  relief=tk.SUNKEN, anchor=tk.W)
        self.statusbar.pack(side=tk.BOTTOM, fill=tk.X)

        self.file_button = tk.Button(self, text=self.file_type,
                                     command=self.get_file)
        self.file_button.pack()
        self.pack()

    def get_file(self):
        self.filename = self.dialog_open.show()
        self.statusbar.config(text=self.file_type + self.filename)


if __name__ == '__main__':
    root = tk.Tk(className=u'calculator')
    data_frm = FileFrame(u'数据文件', master=root)
    result_frm = FileFrame(u'结果文件', master=root)

    root.mainloop()
