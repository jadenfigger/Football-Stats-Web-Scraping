from gui import GuiController
import tkinter as tk

if __name__ == '__main__':
    window = tk.Tk()
    controller = GuiController(window)

    controller.main_window()

