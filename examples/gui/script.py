import tkinter as tk

class ScriptWindow(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        self.label = tk.Label(self, text="Script")
        self.label.pack()
