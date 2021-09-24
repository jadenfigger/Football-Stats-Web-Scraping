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

		# Initializing the title font and default font
		self.title_font = tkFont.Font(family='Ebrima', size=30, weight='bold')
		self.window.option_add('*font', 'Roboto 22')

		# Lists that will contain all the wigets in a certain sction of the gui
		self.main_frame_contents = []
		self.bottom_frame_contents = []
		self.start_frame_buttons = []

		# Value for the slider in the create league window
		self.team_count_slider = None
		# List containing each entry box for inputing team names
		self.team_entrys_frame = None
		self.team_entry_values = []

		# Nummber lookup for the current state of the main frame. 
		# Blank = 0, Create League = 1, add player = 2
		self.main_frame_index = 0
		# Nummber lookup for the current state of the bottom frame. 
		# Blank = 0, show roster = 1
		self.bottom_frame_index = 0

		# Frames for the main window
		self.top_frame = tk.Frame(self.window)
		self.start_frame = tk.Frame(self.window)
		self.bottom_frame = tk.Frame(self.window)


	def dis_start_window(self):
		self.clear_contents(self.window)

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
		self.team_entrys_frame = tk.Frame(m_frame)
		b_frame = tk.Frame(self.window)

		tk.Label(self.window, text="Create League", font=self.title_font, bg=self.BACKGROUND_COLOR, fg=self.TITLE_TEXT_COLOR).grid(
			column=0, row=0, padx=self.UNIV_PADDING, pady=self.UNIV_PADDING)

		# Display slider label
		Label(m_frame, text="Enter Board Size:", bg=self.BACKGROUND_COLOR, fg=self.BUTTON_TEXT_COLOR,).grid(column=0, row=0)
		# Display slider
		self.team_count_slider = tk.Scale(m_frame, from_=2, to=10, orient=tk.HORIZONTAL, bg=self.BACKGROUND_COLOR, fg=self.BUTTON_TEXT_COLOR,
		activebackground=self.BACKGROUND_COLOR, troughcolor=self.BUTTON_COLOR, width=20, command=self.dis_team_entrys)
		self.team_count_slider.grid(column=0, row=1, sticky="nsew", padx=self.UNIV_PADDING, pady=self.UNIV_PADDING)

		self.dis_team_entrys(self.team_count_slider.get())

		# Display start and return buttons
		tk.Button(b_frame, text="Return", command=self.dis_start_window,
		 bg=self.BUTTON_COLOR, fg=self.BUTTON_TEXT_COLOR).grid(column=0, row=0, sticky='nsew', padx=5)
		tk.Button(b_frame, text="Create", command=lambda x=self.team_count_slider.get(): self.dis_main_menu(x),
		 bg=self.BUTTON_COLOR, fg=self.BUTTON_TEXT_COLOR).grid(column=1, row=0, sticky='nsew', padx=5)

		m_frame.grid(column=0, row=1, pady=self.UNIV_PADDING, padx=self.UNIV_PADDING)
		self.team_entrys_frame.grid(column=0, row=2, pady=self.UNIV_PADDING, padx=self.UNIV_PADDING)
		b_frame.grid(column=0, row=2, pady=self.UNIV_PADDING, padx=self.UNIV_PADDING)

		m_frame.configure(bg=self.BACKGROUND_COLOR, highlightthickness=2)
		self.team_entrys_frame.configure(bg=self.BACKGROUND_COLOR)
		b_frame.configure(bg=self.BACKGROUND_COLOR)


	def dis_main_menu(self, num_of_teams):
		pass

	def dis_team_entrys(self, variable):
		team_count = int(variable)

		self.clear_contents(self.team_entrys_frame)

		for i in range(team_count):
			tk.Label(self.team_entrys_frame, text=f'Team Name {i+1}: ', bg=self.BACKGROUND_COLOR, fg=self.BUTTON_TEXT_COLOR).grid(
			 column=0, row=i)
			self.team_entry_values.append(tk.Entry(self.team_entrys_frame, width=17))
			self.team_entry_values[-1].grid(column=1, row=i, pady=5, padx=5)


	def clear_contents(self, list):
		for widget in list.winfo_children():
			widget.destroy()

		self.top_frame = tk.Frame(self.window)
		self.start_frame = tk.Frame(self.window)
		self.bottom_frame = tk.Frame(self.window)