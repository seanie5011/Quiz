'''
A quiz app that allows the user to select a quiz and take an MCQ
'''

# IMPORTS

import customtkinter as ctk
from settings import *
from backend import Quiz

# EXTRA SETTINGS

# set to dark appearance mode
# to use system default, set to 'system'
ctk.set_appearance_mode("dark")

# CLASSES

class HomeTab(ctk.CTkFrame):
	def __init__(self, master, **kwargs):
		'''
		'''
		super().__init__(master, **kwargs)

		# configure background
		self.configure(fg_color=QUESTION_BG_COLOR)

		# set grid weights
		self.grid_columnconfigure(0, weight=1)
		self.grid_rowconfigure((0, 1), weight=1)

		# BODY

		# set title of question
		self.title = ctk.CTkLabel(
			self, 
			text='How does this Quiz App work?',
			font=(FONT_NAME, 50),
		)
		self.title.grid(row=0, column=0, padx=20, pady=0, sticky="ew")

		# set text
		self.text = ctk.CTkLabel(
			self, 
			text='Select one of the above tabs to start each quiz.\n\nThe section quizzes (other tabs!) contain every\nquestion from that section.\n\nThe Random Quiz has 10 questions from any Section.',
			justify='left',
			font=(FONT_NAME, 25),
		)
		self.text.grid(row=1, column=0, padx=20, pady=0, sticky="new")

class Questions(ctk.CTkFrame):
	def __init__(self, master, questions, answers, correct_indices, **kwargs):
		'''
		question: list of strings of the questions to ask
		answers: list of list of strings of the answers (wrong and correct)
		correct_indices: list of indices corresponding to the correct answer in the answers lists
		'''
		super().__init__(master, **kwargs)

		# collect variables
		self.questions = questions
		self.answers = answers
		self.correct_indices = correct_indices

		# configure background
		self.configure(fg_color=QUESTION_BG_COLOR)

		# set grid weights
		self.grid_columnconfigure(0, weight=1)
		self.grid_rowconfigure(0, weight=3)
		self.grid_rowconfigure(1, weight=1)
		self.grid_rowconfigure((2, 3, 4), weight=1)
		self.grid_rowconfigure(5, weight=3)

		# score to keep track of correct answers
		self.score = 0

		# first question initialise at first index
		self.question_index = 0
		self.question(self.questions[self.question_index], self.answers[self.question_index], self.correct_indices[self.question_index], 'unanswered')

	def reset_frame(self):
	    # destroy all widgets from frame
	    for widget in self.winfo_children():
	       widget.destroy()

	def question(self, question, answers, correct_index, question_state, **kwargs):
		'''
		Creates the question frame, with buttons to manage state to next question.

		question: a string of the question to ask
		answers: a list of strings of the potential answers
		correct_index: the index corresponding to which answer is correct in the answers list
		question_state: a string determining what is show (see following)

		if question_state is 'unanswered':
			- the answer buttons are enabled
			- the next question button is disabled
		if question_state is 'wrong':
			- the answer buttons are disabled
			- the next question button is enabled
		if question_state is 'correct':
			- the answer buttons are disabled
			- the next question button is enabled

		There are also some style differences between each.
		'''

		# set title of question
		title = ctk.CTkLabel(
			self, 
			text=f"Question {self.question_index + 1}",
			font=(FONT_NAME, 35),
		)
		title.grid(row=0, column=0, padx=20, pady=0, sticky="ew")

		# set question label
		question = ctk.CTkLabel(
			self, 
			text=question,
			font=(FONT_NAME, 20),
		)
		question.grid(row=1, column=0, padx=20, pady=0, sticky="new")

		# check question state
		# COULD BE SECTIONED FURTHER (but sure look)
		if question_state == 'unanswered':
			# set all answer buttons
			for i, answer in enumerate(answers):
				# check if this is the correct button
				if i == correct_index:
					# create button
					answer_button = ctk.CTkButton(
						self, 
						text=answer, 
						command=self.correct_answer_event,
						border_width=1,
						fg_color=BUTTON_BG_COLOR,
						border_color=BUTTON_BORDER_COLOR_UNANSWERED,
						font=(FONT_NAME, 15),
					)
				else:
					# create button
					answer_button = ctk.CTkButton(
						self, 
						text=answer, 
						command=self.wrong_answer_event,
						border_width=1,
						fg_color=BUTTON_BG_COLOR,
						border_color=BUTTON_BORDER_COLOR_UNANSWERED,
						font=(FONT_NAME, 15),
					)
				# set in grid (2+i as must start from 2)
				answer_button.grid(row=2+i, column=0, padx=20, pady=0, sticky="new")

			# next question button
			next_question_button = ctk.CTkButton(
				self, 
				text='Next Question', 
				command=self.next_question_event,
				state='disabled',
				border_width=1,
				fg_color=BUTTON_BG_COLOR,
				border_color=BUTTON_BORDER_COLOR_UNANSWERED,
				font=(FONT_NAME, 15),
			)
			# set in grid
			next_question_button.grid(row=5, column=0, padx=20, pady=0)
		elif question_state == 'answered':
			# set all answer buttons
			for i, answer in enumerate(answers):
				# check if this is the correct button
				if i == correct_index:
					# create button
					answer_button = ctk.CTkButton(
						self, 
						text=answer, 
						command=self.correct_answer_event,
						state='disabled',
						border_width=1,
						fg_color=BUTTON_BG_COLOR,
						border_color=BUTTON_BORDER_COLOR_CORRECT,
						font=(FONT_NAME, 15),
					)
				else:
					# create button
					answer_button = ctk.CTkButton(
						self, 
						text=answer, 
						command=self.wrong_answer_event,
						state='disabled',
						border_width=1,
						fg_color=BUTTON_BG_COLOR,
						border_color=BUTTON_BORDER_COLOR_WRONG,
						font=(FONT_NAME, 15),
					)

				# set in grid (2+i as must start from 2)
				answer_button.grid(row=2+i, column=0, padx=20, pady=0, sticky="new")

			# next question button
			next_question_button = ctk.CTkButton(
				self, 
				text='Next Question', 
				command=self.next_question_event,
				border_width=1,
				fg_color=BUTTON_BG_COLOR,
				border_color=BUTTON_BORDER_COLOR_UNANSWERED,
				font=(FONT_NAME, 15),
			)
			# set in grid
			next_question_button.grid(row=5, column=0, padx=20, pady=0)

	def correct_answer_event(self):
		# resets frame to be rebuilt
		self.reset_frame()

		# increase score
		self.score += 1

		# remake question in correct answer mode
		self.question(self.questions[self.question_index], self.answers[self.question_index], self.correct_indices[self.question_index], 'answered')

	def wrong_answer_event(self):
		# resets frame to be rebuilt
		self.reset_frame()

		# remake question in wrong answer mode
		self.question(self.questions[self.question_index], self.answers[self.question_index], self.correct_indices[self.question_index], 'answered')

	def next_question_event(self):
		# resets frame to be rebuilt
		self.reset_frame()

		# update question index
		self.question_index += 1
		# if still more questions to go through, next one
		if self.question_index < len(self.questions):
			# make next question
			self.question(self.questions[self.question_index], self.answers[self.question_index], self.correct_indices[self.question_index], 'unanswered')
		# go to finish screen
		else:
			self.finish()

	def finish(self):
		# set title
		title = ctk.CTkLabel(
			self, 
			text="Quiz Finished",
			font=(FONT_NAME, 35),
		)
		title.grid(row=0, column=0, padx=20, pady=0, sticky="ew")

		# set score label
		score = ctk.CTkLabel(
			self, 
			text=f"{self.score} / {len(self.questions)}",
			font=(FONT_NAME, 50),
		)
		score.grid(row=2, column=0, padx=20, pady=0, sticky="new")

		# set info label
		info = ctk.CTkLabel(
			self, 
			text="Think you can do better? Go back to the Home tab before trying again!",
			font=(FONT_NAME, 20),
		)
		info.grid(row=4, column=0, padx=20, pady=0, sticky="new")

class Sections(ctk.CTkTabview):
	def __init__(self, master, quiz_filepath, **kwargs):  # keep kwargs so can use command attribute
		'''
		quiz_filepath: string of the path to the .txt file for the quiz
		'''
		super().__init__(master, **kwargs)

		# instantiate a quiz instance for this text file
		self.quiz = Quiz(quiz_filepath)

		# configure background
		self.configure(fg_color=BG_COLOR)

		# first tab is Home with information
		self.add('Home')
		# set grid weights
		self.tab('Home').grid_columnconfigure(0, weight=1)
		self.tab('Home').grid_rowconfigure(0, weight=1)

		# second tab is random questions quiz
		self.add('Random Quiz')
		# set grid weights
		self.tab('Random Quiz').grid_columnconfigure(0, weight=1)
		self.tab('Random Quiz').grid_rowconfigure(0, weight=1)

		# create tabs based on sections
		for i, section in enumerate(self.quiz.get_sections()):
			# add the tab for this section
			self.add(section)
			# set grid weights
			self.tab(section).grid_columnconfigure(0, weight=1)
			self.tab(section).grid_rowconfigure(0, weight=1)

		# create tab selection callback
		self.configure(command=self.tab_click)

		# set current tab to home
		self.set('Home')
		# this frame is what is currently displayed
		# it will be destroyed and recreated depending on what needs to be shown
		self.active_frame = HomeTab(self.tab('Home'))
		self.active_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

	# sets the frame for this tab
	def tab_click(self):
		# destroy currently active frame
		self.active_frame.destroy()

		# get name of tab
		current_tab = self.get()

		# if home tab
		if current_tab == 'Home':
			# contains information on quiz

			# home screen
			self.active_frame = HomeTab(self.tab(current_tab))
			self.active_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
		# if random tab
		elif current_tab == 'Random Quiz':
			# create a random quiz

			# pull question data from all sections
			questions, answers, correct_indices = self.quiz.get_random_quiz()
			
			# create the frame
			self.active_frame = Questions(self.tab(current_tab), questions, answers, correct_indices)
			self.active_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
		# if a section tab
		else:
			# create a section quiz

			# pull question data from a particular section
			# have to convert name to section key
			questions, answers, correct_indices = self.quiz.get_section_quiz(self.quiz.get_section_key_by_name(current_tab))

			# create the frame
			self.active_frame = Questions(self.tab(current_tab), questions, answers, correct_indices)
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
		self.tab_view = Sections(self, 'assets/data/ClinicalPracticeWorkbook.txt')
		self.tab_view.grid(row=0, column=0, padx=0, pady=0, sticky='nesw')

		# MAIN LOOP

		self.mainloop()

# RUNNING

if __name__ == '__main__':
	App()