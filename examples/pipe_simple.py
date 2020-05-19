import vibrance
import vibrance.pipe

PALETTE = (
    "000000",  # black
    "FFFFFF",  # white
    "FF0000",  # red
    "00FF00",  # green
    "0000FF",  # blue
    "FFFF00",  # yellow
    "00FFFF",  # cyan
    "FF00FF",  # magenta
    "FF8000",  # orange
    "8000FF",  # purple
    "0080FF",  # light blue
    "FF0080",  # pink
)

PORTS = list(range(9001, 9007))

api = vibrance.pipe.PipeInterface()

@api.handle
def cycle(obj):
    i = obj

    api.color((9001, 9004), PALETTE[i])
    api.color((9002, 9003, 9005, 9006), "000")
    api.wait(0.5)

    api.color((9002, 9005), PALETTE[i])
    api.color((9001, 9003, 9004, 9006), "000")
    api.wait(0.5)

    api.color((9003, 9006), PALETTE[i])
    api.color((9001, 9002, 9004, 9005), "000")
    api.wait(0.5)

    api.color((9002, 9005), PALETTE[i])
    api.color((9001, 9003, 9004, 9006), "000")

@api.handle
def chase(obj):
    i = obj

    for port in (9003, 9002, 9001, 9004, 9005, 9006):
        api.color(port, PALETTE[i])
        api.color([p for p in PORTS if p != port], "000")
        api.wait(0.1)

@api.handle
def clear():
    api.color(PORTS, "000")

@api.onTelemetry
def onTelemetry(telemetry):
    print(telemetry)

if __name__ == "__main__":
    import sys
    import multiprocessing
    import tkinter as tk

    ctrl = vibrance.Controller()
    ctrl.connect(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None)

    pipe = vibrance.pipe.PipeInput()

    api_proc = multiprocessing.Process(target=api.run, args=(pipe, ctrl))
    api_proc.start()

    root = tk.Tk()

    cycleButton = tk.Button(text="cycle",
                            command=lambda: pipe.launch("cycle", 6))
    cycleButton.pack()

    chaseButton = tk.Button(text="chase",
                            command=lambda: pipe.launch("chase", 7))
    chaseButton.pack()

    clearButton = tk.Button(text="clear",
                            command=lambda: pipe.launch("clear"))
    clearButton.pack()

    tk.mainloop()
