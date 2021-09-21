import tkinter as tk

class GuiController:
	def __init__(self, win):
		BACKGROUND_COLOR = 'FFFFFF'
		FRAME_COLOR = None
		BUTTON_COLOR = None
		BUTTON_PRESSED = None
		BUTTON_HOVORED = None

		self.window = win

		self.main_frame_contents = []
		self.bottom_frame_contents = []

		self.top_frame = tk.Frame(self.window)
		self.start_frame = tk.Frame(self.top_frame)
		self.main_frame = tk.Frame(self.top_frame)
		self.bottom_frame = tk.Frame(self.window)

	def main_window(self):
		pass
