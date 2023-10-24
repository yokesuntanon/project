import tkinter as tk

window = tk.Tk()
window.title("App")

button_1 = tk.Button(master=window, text="Tax")
button_2 = tk.Button(master=window, text="Comparison")

button_1.pack()
button_2.pack()

window.mainloop()