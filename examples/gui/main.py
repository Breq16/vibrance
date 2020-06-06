import tkinter as tk

import script, input, relay

class MainWindow(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        for i in range(3):
            tk.Grid.columnconfigure(self, i, weight=1)

        self.input = input.InputWindow(self)
        self.script = script.ScriptWindow(self)
        self.relay = relay.RelayWindow(self)

        self.input.grid(row=0, column=0, sticky=tk.N+tk.E+tk.S+tk.W)
        self.script.grid(row=0, column=1, sticky=tk.N+tk.E+tk.S+tk.W)
        self.relay.grid(row=0, column=2, sticky=tk.N+tk.E+tk.S+tk.W)



if __name__ == "__main__":
    root = tk.Tk()
    MainWindow(root).pack(fill=tk.BOTH, expand=True)
    root.mainloop()
