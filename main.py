from gui import GuiController
from sql_db_creation import sqlController
import tkinter as tk

if __name__ == '__main__':
    window = tk.Tk()
    window.option_add( "*font", "roboto 22")

    sqlCon = sqlController()

    controller = GuiController(window, sqlCon)

    controller.dis_window()

