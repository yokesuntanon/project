import tkinter as tk


class TaxWindow:
    def __init__(self) -> None:
        self.window = tk.Tk()
        self.window.title("Tax")
        self.window.mainloop()

window = tk.Tk()
window.title("App")

button_1 = tk.Button(master=window, text="Tax", command=TaxWindow)
button_2 = tk.Button(master=window, text="Comparison")

button_1.pack()
button_2.pack()

window.mainloop()