import tkinter as tk
from tkinter import ttk

class GuiController:
	BACKGROUND_COLOR = '#0096c7'
	FRAME_COLOR = '#ade8f4'
	BUTTON_COLOR = None
	BUTTON_PRESSED = None
	BUTTON_HOVORED = None
	BUTTON_TEXT_COLOR = '#1c1c1c'

	UNIV_PADDING = 10
	def __init__(self, win, sqlCon):
		self.window = win
		self.sqlController = sqlCon

		self.main_frame_contents = []
		self.bottom_frame_contents = []
		self.start_frame_buttons = []

		# Nummber lookup for the current state of the main frame. 
		# Blank = 0, Create League = 1, add player = 2
		self.main_frame_index = 0
		# Nummber lookup for the current state of the bottom frame. 
		# Blank = 0, show roster = 1
		self.bottom_frame_index = 0

		self.top_frame = tk.Frame(self.window)
		self.start_frame = tk.Frame(self.top_frame)
		self.main_frame = tk.Frame(self.top_frame)
		self.bottom_frame = tk.Frame(self.window)

		self.tab_control = ttk.Notebook(self.main_frame)


	def dis_window(self):
		self.window.configure(bg=self.BACKGROUND_COLOR)

		self.start_frame_buttons.append(tk.Button(self.start_frame, text="Create New League",
		 bg=self.BUTTON_COLOR, fg=self.BUTTON_TEXT_COLOR))
		self.start_frame_buttons[-1].grid(column=0, row=0, sticky="nsew", padx=self.UNIV_PADDING, pady=self.UNIV_PADDING)
		self.start_frame_buttons.append(tk.Button(self.start_frame, text="Open Existing League",
		 bg=self.BUTTON_COLOR, fg=self.BUTTON_TEXT_COLOR))
		self.start_frame_buttons[-1].grid(column=0, row=2, sticky="nsew", padx=self.UNIV_PADDING, pady=self.UNIV_PADDING)

		if (self.main_frame_index == 0):
			self.dis_empty_main()
			


		self.top_frame.grid(column=0, row=0, padx=self.UNIV_PADDING, pady=self.UNIV_PADDING)
		self.start_frame.grid(column=0, row=0, padx=self.UNIV_PADDING, pady=self.UNIV_PADDING)
		self.main_frame.grid(column=1, row=0, padx=self.UNIV_PADDING, pady=self.UNIV_PADDING)
		self.bottom_frame.grid(column=0, row=1, padx=self.UNIV_PADDING, pady=self.UNIV_PADDING)

		self.top_frame.configure(bg=self.BACKGROUND_COLOR)
		self.start_frame.configure(bg=self.BACKGROUND_COLOR, highlightthickness=2)
		self.main_frame.configure(bg=self.BACKGROUND_COLOR)
		self.bottom_frame.configure(bg=self.BACKGROUND_COLOR)


		self.window.mainloop()
	
	def dis_empty_main(self):
		tab1 = ttk.Frame(self.tab_control)
		tk.Button(tab1, text="Choose League").grid(column=0, row=0)

		self.tab_control.add(tab1, text="Tab 1")
		self.tab_control.grid(column=0, row=0)




	def clear_contents(list):
		for widget in list.winfo_children():
			widget.destroy()