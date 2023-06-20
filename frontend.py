'''
A quiz app that allows the user to select a quiz and take an MCQ
'''

# IMPORTS

import customtkinter as ctk
from settings import *

# EXTRA SETTINGS

# set to dark appearance mode
# to use system default, set to 'system'
ctk.set_appearance_mode("dark")

# CLASSES

class Question(ctk.CTkFrame):
	def __init__(self, master, question_index, question, answers, correct_index, **kwargs):
		'''
		question_index: int of whether this is question 0, 1, 2, etc.
		question: string of the question to ask
		answers: list of strings of the answers (wrong and correct)
		correct_index: the index corresponding to the correct answer in the answers list
		'''
		super().__init__(master, **kwargs)

		# collect variables
		self.question_index = question_index
		self.question = question
		self.answers = answers
		self.correct_index = correct_index

		# store answer buttons
		self.answer_buttons = []

		# configure background
		self.configure(fg_color=QUESTION_BG_COLOR)

		# set grid weights
		self.grid_columnconfigure(0, weight=1)
		self.grid_rowconfigure(0, weight=3)
		self.grid_rowconfigure(1, weight=2)
		self.grid_rowconfigure((2, 3, 4), weight=1)

		# BODY

		# set title of question
		self.title = ctk.CTkLabel(
			self, 
			text=f"Question {self.question_index}",
		)
		self.title.grid(row=0, column=0, padx=20, pady=0, sticky="ew")

		# set question label
		self.question = ctk.CTkLabel(
			self, 
			text=self.question,
		)
		self.question.grid(row=1, column=0, padx=20, pady=0, sticky="new")

		# set all answer buttons
		for i, answer in enumerate(answers):
			# create button
			answer_button = ctk.CTkButton(
				self, 
				text=answer, 
				command=self.answer_event
			)
			# set in grid (2+i as must start from 2)
			answer_button.grid(row=2+i, column=0, padx=20, pady=0, sticky="new")
			# store in list
			self.answer_buttons.append(answer_button)

	def answer_event(self):
		pass

class Sections(ctk.CTkTabview):
	def __init__(self, master, sections, **kwargs):  # keep kwargs so can use command attribute
		'''
		sections: list of strings of all the sections names
		'''
		super().__init__(master, **kwargs)

		# collect variables
		self.sections = sections

		# configure background
		self.configure(fg_color=BG_COLOR)

		# first tab is random questions quiz
		self.add('Random Quiz')
		# set grid weights
		self.tab('Random Quiz').grid_columnconfigure(0, weight=1)
		self.tab('Random Quiz').grid_rowconfigure(0, weight=1)

		# create tabs based on sections
		for i, section in enumerate(sections):
			# add the tab for this section
			self.add(section)
			# set grid weights
			self.tab(section).grid_columnconfigure(0, weight=1)
			self.tab(section).grid_rowconfigure(0, weight=1)

		# create tab selection callback
		self.configure(command=self.tab_click)

		# this frame is what is currently displayed
		# it will be destroyed and recreated depending on what needs to be shown
		self.active_frame = ctk.CTkFrame(self)

	# sets the frame for this tab
	def tab_click(self):
		# destroy currently active frame
		self.active_frame.destroy()

		# get name of tab
		current_tab = self.get()
		# check if section or random tab
		if current_tab == 'Random Quiz':
			# create a random question
			# pull question data from all sections
			print('random!')
			self.active_frame = Question(self.tab(current_tab), 0, "This is a random question", ["wrong", "wrong", "correct"], 2)
			self.active_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
		else:
			# create a section question
			# pull question data from a particular section
			print('section!')
			self.active_frame = Question(self.tab(current_tab), 1, f"This is a question from {current_tab}", ["wrong", "correct", "wrong"], 1)
			self.active_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

# MAIN WINDOW

class App(ctk.CTk):
	'''
	Contains the window for the app.
	'''

	def __init__(self):
		# initialise with foreground color
		super().__init__(fg_color=BG_COLOR)

		# WINDOW PROPERTIES

		self.title('Quiz App')
		self.geometry('900x800')

		# BODY

		# set grid weights
		self.grid_columnconfigure(0, weight=1)
		self.grid_rowconfigure(0, weight=1)

		# set tabs
		self.tab_view = Sections(self, ['Chapter 1', 'Chapter 2'])
		self.tab_view.grid(row=0, column=0, padx=0, pady=0, sticky='nesw')

		# MAIN LOOP

		self.mainloop()

# RUNNING

if __name__ == '__main__':
	App()