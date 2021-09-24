from gui import GuiController
from sql_db_creation import sqlController
import tkinter as tk

if __name__ == '__main__':
    window = tk.Tk()

    sqlCon = sqlController()

    controller = GuiController(window, sqlCon)

    controller.dis_start_window()