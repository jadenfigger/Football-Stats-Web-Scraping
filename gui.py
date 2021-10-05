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

	UNIV_PADDING = 7
	def __init__(self, win, sqlCon):
		# Window creation and option intializations
		self.window = win
		self.window.configure(padx=self.UNIV_PADDING, pady=self.UNIV_PADDING)
		self.window.configure(bg=self.BACKGROUND_COLOR)

		self.sqlController = sqlCon

		# Initializing the title font and default font
		self.d_font_size = 18
		self.title_font = tkFont.Font(family='Ebrima', size=27, weight='bold')
		self.window.option_add('*font', f'Ebrima {self.d_font_size}')

		# Lists that will contain all the wigets in a certain sction of the gui
		self.main_frame_contents = []
		self.bottom_frame_contents = []
		self.start_frame_buttons = []

		# Value for the slider in the create league window
		# List containing each entry box for inputing team names
		self.team_entrys_frame = None

		# Nummber lookup for the current state of the main frame. 
		# Blank = 0, Create League = 1, add player = 2
		self.main_frame_index = 0
		# Nummber lookup for the current state of the bottom frame. 
		# Blank = 0, show roster = 1
		self.bottom_frame_index = 0

		# Frames for the main window
		self.top_frame = tk.Frame(self.window)
		self.start_frame = None
		self.bottom_frame = tk.Frame(self.window)

		self.main_width = 700
		self.main_height = 300


	def dis_start_window(self):
		self.clear_contents(self.window)

		self.start_frame = tk.Frame(self.window)

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
		self.sqlController.team_count_slider = tk.Scale(m_frame, from_=2, to=10, orient=tk.HORIZONTAL, bg=self.BACKGROUND_COLOR, fg=self.BUTTON_TEXT_COLOR,
		activebackground=self.BACKGROUND_COLOR, troughcolor=self.BUTTON_COLOR, width=20, command=self.dis_team_entrys)
		self.sqlController.team_count_slider.grid(column=0, row=1, sticky="nsew", padx=self.UNIV_PADDING, pady=self.UNIV_PADDING)

		self.dis_team_entrys(self.sqlController.team_count_slider.get())

		# Display start and return buttons
		tk.Button(b_frame, text="Return", command=self.dis_start_window,
		 bg=self.BUTTON_COLOR, fg=self.BUTTON_TEXT_COLOR).grid(column=0, row=0, sticky='nsew', padx=5)
		tk.Button(b_frame, text="Create", command=lambda x=self.sqlController.team_count_slider.get(): self.dis_main_menu(x),
		 bg=self.BUTTON_COLOR, fg=self.BUTTON_TEXT_COLOR).grid(column=1, row=0, sticky='nsew', padx=5)

		m_frame.grid(column=0, row=1, pady=self.UNIV_PADDING, padx=self.UNIV_PADDING)
		self.team_entrys_frame.grid(column=0, row=2, pady=self.UNIV_PADDING, padx=self.UNIV_PADDING)
		b_frame.grid(column=0, row=2, pady=self.UNIV_PADDING, padx=self.UNIV_PADDING)

		m_frame.configure(bg=self.BACKGROUND_COLOR, highlightthickness=2)
		self.team_entrys_frame.configure(bg=self.BACKGROUND_COLOR)
		b_frame.configure(bg=self.BACKGROUND_COLOR)


	def dis_main_menu(self, values):
		self.sqlController.team_count_slider = values
		self.sqlController.team_entry_values =  [x.get() for x in self.sqlController.team_entry_values]
		self.sqlController.team_count = values

		for i in range(self.sqlController.team_count_slider):
			self.sqlController.player_id_entries.append([])
			for j in range(12):
				self.sqlController.player_id_entries[i].append(tk.StringVar())
		

		self.clear_contents(self.window)
		self.top_frame = tk.Frame(self.window)
		top_right_frame = tk.Frame(self.top_frame, width=self.main_width, height=self.main_height)
		self.bottom_frame = tk.Frame(self.window)
		bottom_right_frame = tk.Frame(self.bottom_frame, width=self.main_width, height=self.main_height)

		# Title
		tk.Label(self.window, text="Fantasy Football Manager", bg=self.BACKGROUND_COLOR,
		 fg=self.TITLE_TEXT_COLOR, font=self.title_font).grid(column=0, row=0, sticky='nsew')

		self.dis_fill_team(0, top_right_frame)
		
		self.top_frame.grid(column=0, row=1, pady=self.UNIV_PADDING, padx=self.UNIV_PADDING)
		self.bottom_frame.grid(column=0, row=2, pady=self.UNIV_PADDING, padx=self.UNIV_PADDING)
		top_right_frame.grid(column=0, row=0, pady=self.UNIV_PADDING, padx=self.UNIV_PADDING)
		bottom_right_frame.grid(column=0, row=0, pady=self.UNIV_PADDING, padx=self.UNIV_PADDING)

		self.top_frame.configure(bg=self.BACKGROUND_COLOR)
		self.bottom_frame.configure(bg=self.BACKGROUND_COLOR)
		top_right_frame.configure(bg=self.FRAME_COLOR)
		bottom_right_frame.configure(bg=self.FRAME_COLOR)


	def dis_fill_team(self, index, frame):
		left_frame = tk.Frame(frame)
		right_frame = tk.Frame(frame)

		team_label = tk.Label(frame, text=f"{self.sqlController.team_entry_values[index]}", bg=self.FRAME_COLOR, 
		 fg=self.BUTTON_TEXT_COLOR, font=self.title_font)
		team_label.grid(column=0, row=0, columnspan=2)

		tk.Label(right_frame, text="Starter", bg=self.FRAME_COLOR, fg=self.BUTTON_TEXT_COLOR,
		 font=('Ebrima 20 bold')).grid(column=1, row=0)
		tk.Label(right_frame, text="Backup", bg=self.FRAME_COLOR, fg=self.BUTTON_TEXT_COLOR,
		 font=('Ebrima 20 bold')).grid(column=2, row=0)

		tk.Label(right_frame, text="QB1:", background=self.FRAME_COLOR, fg=self.BUTTON_TEXT_COLOR,
		 font=(f'Ebrima {self.d_font_size} bold')).grid(column=0, row=1, padx=2, pady=2)
		tk.Label(right_frame, text="QB2:", background=self.FRAME_COLOR, fg=self.BUTTON_TEXT_COLOR,
		 font=(f'Ebrima {self.d_font_size} bold')).grid(column=0, row=2, padx=2, pady=2)
		tk.Label(right_frame, text="RB1:", background=self.FRAME_COLOR, fg=self.BUTTON_TEXT_COLOR,
		 font=(f'Ebrima {self.d_font_size} bold')).grid(column=0, row=3, padx=2, pady=2)
		tk.Label(right_frame, text="RB2:", background=self.FRAME_COLOR, fg=self.BUTTON_TEXT_COLOR,
		 font=(f'Ebrima {self.d_font_size} bold')).grid(column=0, row=4, padx=2, pady=2)
		tk.Label(right_frame, text="WR1:", background=self.FRAME_COLOR, fg=self.BUTTON_TEXT_COLOR,
		 font=(f'Ebrima {self.d_font_size} bold')).grid(column=0, row=5, padx=2, pady=2)
		tk.Label(right_frame, text="WR2:", background=self.FRAME_COLOR, fg=self.BUTTON_TEXT_COLOR,
		 font=(f'Ebrima {self.d_font_size} bold')).grid(column=0, row=6, padx=2, pady=2)

		for i in range(1, 7):
			tk.Entry(right_frame, text="Player ID", textvariable=self.sqlController.player_id_entries[index][(i-1)*2]).grid(
			 column=1, row=i, padx=3, pady=3)
			tk.Entry(right_frame, text="Player ID", textvariable=self.sqlController.player_id_entries[index][((i-1)*2)-1]).grid(
			 column=2, row=i, padx=3, pady=3)

		 
		pre_button = tk.Button(left_frame, text='Previous', bg=self.BUTTON_COLOR, fg=self.BUTTON_TEXT_COLOR,
		 command=lambda x=index: move_backwards(x), state=tk.DISABLED)
		pre_button.grid(column=0, row=0, sticky='nsew', padx=3, pady=10)
		next_button = tk.Button(left_frame, text='Next', bg=self.BUTTON_COLOR, fg=self.BUTTON_TEXT_COLOR, 
		 command=lambda x=index: move_forward(x))
		next_button.grid(column=0, row=1, sticky='nsew', padx=3, pady=10)
		submit_button = tk.Button(left_frame, text='Submit', bg=self.BUTTON_COLOR, fg=self.BUTTON_TEXT_COLOR,
		 command=lambda: team_players_submit())
		submit_button.grid(column=0, row=2, sticky='nsew', padx=3, pady=10)

		left_frame.grid(column=0, row=1, padx=self.UNIV_PADDING, pady=self.UNIV_PADDING)
		right_frame.grid(column=1, row=1, padx=self.UNIV_PADDING, pady=self.UNIV_PADDING)

		left_frame.configure(bg=self.FRAME_COLOR, width=self.main_width, height=self.main_height)
		right_frame.configure(bg=self.FRAME_COLOR, width=self.main_width, height=self.main_height)


		def move_forward(index):
			if (index >= 0):
				index += 1
				next_button.configure(state=tk.NORMAL)
				pre_button.configure(state=tk.NORMAL)
				team_label.configure(text=f"{self.sqlController.team_entry_values[index]}")
			if (index >= self.sqlController.team_count_slider-1):
				next_button.configure(state=tk.DISABLED)
				pre_button.configure(state=tk.NORMAL)
				index = self.sqlController.team_count_slider-1
			
		def move_backwards(index):
			if (index >= self.sqlController.team_count_slider-1):
				index -= 1
				next_button.configure(state=tk.NORMAL)
				pre_button.configure(state=tk.NORMAL)
				team_label.configure(text=f"{self.sqlController.team_entry_values[index]}")
			if (index <= 0):
				next_button.configure(state=tk.NORMAL)
				pre_button.configure(state=tk.DISABLED)
				index = 0

		def team_players_submit():
			self.sqlController.create_team_dict()


	def dis_team_entrys(self, variable):
		team_count = int(variable)
		self.clear_contents(self.team_entrys_frame)


		for i in range(team_count):
			tk.Label(self.team_entrys_frame, text=f'Team Name {i+1}: ', bg=self.BACKGROUND_COLOR, fg=self.BUTTON_TEXT_COLOR).grid(
			 column=0, row=i)
			self.sqlController.team_entry_values.append(tk.Entry(self.team_entrys_frame, width=17))
			self.sqlController.team_entry_values[-1].grid(column=1, row=i, pady=5, padx=5)


	def clear_contents(self, list):
		for widget in list.winfo_children():
			widget.destroy()