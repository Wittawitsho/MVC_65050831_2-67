import tkinter as tk
from controller import DriverController

if __name__ == "__main__":
    root = tk.Tk()
    app = DriverController(root)
    root.mainloop()
