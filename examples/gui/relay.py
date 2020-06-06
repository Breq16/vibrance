import tkinter as tk

class RelayWindow(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        self.label = tk.Label(self, text="Relay")
        self.label.pack()
