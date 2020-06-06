import tkinter as tk

class InputWindow(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        self.label = tk.Label(self, text="Input")
        self.label.pack()

        self.inputType = tk.StringVar()
        self.optionmenu = tk.OptionMenu(self, self.inputType, "MIDI", "UART")
        self.optionmenu.pack()
