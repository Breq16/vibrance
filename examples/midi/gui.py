import tkinter as tk

root = tk.Tk()

input_frame = tk.Frame(root, relief=tk.RIDGE, borderwidth=10)

plugin_frame = tk.Frame(root, relief=tk.RIDGE, borderwidth=10)

output_frame = tk.Frame(root, relief=tk.RIDGE, borderwidth=10)

input_frame.grid(row=0, column=0, sticky=tk.N+tk.E+tk.S+tk.W)
plugin_frame.grid(row=0, column=1, sticky=tk.N+tk.E+tk.S+tk.W)
output_frame.grid(row=0, column=2, sticky=tk.N+tk.E+tk.S+tk.W)

for x in range(3):
    tk.Grid.columnconfigure(root, x, weight=1)
tk.Grid.rowconfigure(root, 0, weight=1)

BIG_FONT = ("Ubuntu", 24)

## INPUT FRAME
tk.Label(input_frame, text="Input", font=BIG_FONT).pack(ipadx=10, ipady=10)

input_var = tk.StringVar()
tk.OptionMenu(input_frame, input_var, "MIDI", "UART").pack()

midi_frame = tk.Frame(input_frame)
midi_port = tk.StringVar()
tk.Label(midi_frame, text="MIDI Port Name:").pack()
tk.Entry(midi_frame, textvariable=midi_port).pack()

uart_frame = tk.Frame(input_frame)
uart_port = tk.StringVar()
tk.Label(uart_frame, text="UART Port:").pack()
tk.OptionMenu(uart_frame, uart_port, "/dev/ttyACM0", "/dev/ttyUSB0").pack()

def show_frame(name1, name2, op):
    if input_var.get() == "MIDI":
        uart_frame.pack_forget()
        midi_frame.pack()
    elif input_var.get() == "UART":
        midi_frame.pack_forget()
        uart_frame.pack()
input_var.trace("w", show_frame)

## PLUGIN FRAME
tk.Label(plugin_frame, text="Plugin", font=BIG_FONT).pack(ipadx=10, ipady=10)

plugin_var = tk.StringVar()
tk.OptionMenu(plugin_frame, plugin_var, "Simple", "Animations", "Big Brain").pack()

## OUTPUT FRAME
tk.Label(output_frame, text="Output", font=BIG_FONT).pack(ipadx=10, ipady=10)

tk.Label(output_frame, text="Relay IP:").pack()
ctrl_addr = tk.StringVar()
tk.Entry(output_frame, textvariable=ctrl_addr).pack()

tk.Label(output_frame, text="Password:").pack()
ctrl_psk = tk.StringVar()
tk.Entry(output_frame, textvariable=ctrl_psk).pack()

tk.Button(output_frame, text="Connect").pack()

root.minsize(800, 350)
root.mainloop()
