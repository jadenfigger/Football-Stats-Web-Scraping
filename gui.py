import tkinter as tk
from tkinter import Label, ttk
import tkinter.font as tkFont

class GuiController:
	BACKGROUND_COLOR = '#734C5A'
	FRAME_COLOR = '#FFB5B8'
	BUTTON_COLOR = '#F27E7E'
	BUTTON_PRESSED = '#FF8585'
	BUTTON_TEXT_COLOR = '#000000'
	TITLE_TEXT_COLOR = '#F2E2C4'

	UNIV_PADDING = 10
	def __init__(self, win, sqlCon):
		# Window creation and option intializations
		self.window = win
		self.window.configure(padx=self.UNIV_PADDING, pady=self.UNIV_PADDING)
		self.window.configure(bg=self.BACKGROUND_COLOR)

		self.sqlController = sqlCon

		self.title_font = tkFont.Font(family='Ebrima', size=30, weight='bold')

		self.window.option_add('*font', 'Roboto 22')

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
		self.start_frame = tk.Frame(self.window)
		self.bottom_frame = tk.Frame(self.window)


	def dis_start_window(self):
		tk.Label(self.window, text="Fantasy Football\nLeague Manager", bg=self.BACKGROUND_COLOR,
		font=self.title_font, fg=self.TITLE_TEXT_COLOR).grid(column=0, row=0, padx=self.UNIV_PADDING)

		tk.Button(self.start_frame, text="Create New\nLeague",
		 bg=self.BUTTON_COLOR, fg=self.BUTTON_TEXT_COLOR, activebackground=self.BUTTON_PRESSED, command=self.dis_create_league).grid(
		  column=0, row=0, sticky="nsew", padx=self.UNIV_PADDING*2, pady=self.UNIV_PADDING)
		tk.Button(self.start_frame, text="Open Existing\nLeague",
		 bg=self.BUTTON_COLOR, fg=self.BUTTON_TEXT_COLOR, activebackground=self.BUTTON_PRESSED).grid(
		  column=0, row=1, sticky="nsew", padx=self.UNIV_PADDING*2, pady=self.UNIV_PADDING)

		self.start_frame.grid(column=0, row=1, padx=self.UNIV_PADDING, pady=self.UNIV_PADDING)

		self.start_frame.configure(bg=self.BACKGROUND_COLOR)

		self.window.mainloop()
	
	
	def dis_create_league(self):
		self.clear_contents(self.window)

		m_frame = tk.Frame(self.window)
		b_frame = tk.Frame(self.window)

		tk.Label(self.window, text="Create League", font=self.title_font, bg=self.BACKGROUND_COLOR, fg=self.TITLE_TEXT_COLOR).grid(
			column=0, row=0, padx=self.UNIV_PADDING, pady=self.UNIV_PADDING)

		# Draw slider label
		Label(m_frame, text="Enter Board Size:", bg=self.BACKGROUND_COLOR, fg=self.BUTTON_TEXT_COLOR,).grid(column=0, row=0)
		# Draw slider
		self.gridSlider = tk.Scale(m_frame, from_=2, to=15, orient=tk.HORIZONTAL, bg=self.BACKGROUND_COLOR, fg=self.BUTTON_TEXT_COLOR,
		activebackground=self.BACKGROUND_COLOR, troughcolor=self.BUTTON_COLOR)
		self.gridSlider.grid(column=0, row=1, sticky="nsew", padx=self.UNIV_PADDING, pady=self.UNIV_PADDING)

		m_frame.grid(column=0, row=1)
		b_frame.grid(column=0, row=2)

		m_frame.configure(bg=self.BACKGROUND_COLOR, highlightthickness=2, highlightcolor=self.BUTTON_COLOR)
		b_frame.configure(bg=self.BACKGROUND_COLOR)


	def clear_contents(self, list):
		for widget in list.winfo_children():
			widget.destroy()