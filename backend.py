'''
The text file used should have unique identifiers at the start of each line.
For a section (eg: Chapter 1, Chapter 2, etc), the identifier should be a '='. (there must be atleast one section)
For a question, the identifier should be a '-'. (there must be atleast one question)
For a wrong answer, the identifier should be a '+'. (there must be two wrong answers per question)
For a correct answer, the identifier should be a '_'. (there can be only one correct answer per question)
A section should always be followed by a question, and a question should always be followed by two wrong answers and a correct answer (any order).
'''

# dependancies
from pathlib import Path
import random

# Quiz class to perform operations on text file
class Quiz():
	def __init__(self, filepath):
		# define path to file
		path = Path.cwd() / filepath

		# read in data
		content = path.read_text(encoding="utf-8")
		# split by "\n"
		content = content.splitlines()

		# process into dict
		self.quiz = self.process_content(content)

	def process_content(self, content):
		'''
		Process each string in content into a dictionary.

		content: list of strings in order of the text file

		Each string (line) is processed according to the first character of that string (identifier). \
		If 
		'''
		# where all data is stored
		quiz = {}
		# counters used to keep track of indices
		section_counter = -1
		question_counter = -1
		wrong_counter = -1

		# pass through every line
		for line_index, line in enumerate(content):
		    # get the identifier
		    identifier = line[0]
		    
		    # check if this is a section
		    if identifier == '=':
		        # increase counter
		        section_counter += 1
		        
		        # reset question counter
		        question_counter = -1
		        
		        # update the section count (index so +1)
		        quiz['section count'] = section_counter + 1
		        
		        # add a section
		        quiz[f'section {section_counter}'] = {
		            'name': line[1:],
		            'line index': line_index,
		        }
		    # check if this is a question
		    elif identifier == '-':
		        # increase counter
		        question_counter += 1
		        
		        # reset wrong counter
		        wrong_counter = -1
		        
		        # update this sections question count (index so +1)
		        quiz[f'section {section_counter}']['question count'] = question_counter + 1
		        
		        # add a question to this section
		        quiz[f'section {section_counter}'][f'question {question_counter}'] = {
		            'name': line[1:],
		            'line index': line_index,
		        }
		    # check if this is a wrong answer
		    elif identifier == '+':
		        # increase counter
		        wrong_counter += 1
		        
		        # add a wrong answer to this question
		        quiz[f'section {section_counter}'][f'question {question_counter}'][f'wrong {wrong_counter}'] = {
		            'name': line[1:],
		            'line index': line_index,
		        }
		    # check if this is a correct answer
		    elif identifier == '_':
		        # add a correct answer to this question
		        quiz[f'section {section_counter}'][f'question {question_counter}'][f'correct'] = {
		            'name': line[1:],
		            'line index': line_index,
		        }

		return quiz

	def get_sections(self):
		'''
		Returns the name of each section (list of strings).
		'''

		# store all names
		names = []
		# use section count to pass through each section
		for section_index in range(self.quiz['section count']):
			# get each question by using section count to get index
			# append name to list
			names.append(self.quiz[f'section {section_index}']['name'])

		return names

	def get_section_key_by_name(self, name):
		'''
		Passes through each section and matches the section name to the section key. \
		Returns a string of the section key.

		Definitely inefficient but hey it works!
		'''

		# use section count to pass through each section
		for section_index in range(self.quiz['section count']):
			# get each question by using section count to get index
			# if name matches, return the section key string
			if name == self.quiz[f'section {section_index}']['name']:
				return f'section {section_index}'

	def get_all_questions_dicts(self):
		'''
		Returns a list of dicts corresponding to every question in all sections.
		'''

		# store all question dictionaries in a list
		question_dicts = []
		# use section count to pass through each section
		for section_index in range(self.quiz['section count']):
			# get each question by using section count to get index
			for question_index in range(self.quiz[f'section {section_index}']['question count']):
				# append to list
				question_dicts.append(self.quiz[f'section {section_index}'][f'question {question_index}'])

		return question_dicts

	def get_questions_from_section(self, section):
		'''
		Returns a list of dicts corresponding to every question in a given section.
		'''

		# store all question dictionaries in a list
		question_dicts = []
		# get each question by using section count to get index
		for question_index in range(self.quiz[section]['question count']):
			# append to list
			question_dicts.append(self.quiz[section][f'question {question_index}'])

		return question_dicts

	def process_question_dicts(self, question_dicts):
		'''
		This returns a list of questions, a list of answers, and a list of correct indices. \
		These correspond to the list of question dictonaries supplied.

		Returns:
		- a list of strings
		- a list of lists of strings
		- a list of integers
		'''

		# extract data from these and store in lists
		questions = []
		answers = []
		correct_indices = []
		# answer keys, these will be shuffled when extracting answers for randomisation
		answer_keys = ['wrong 0', 'wrong 1', 'correct']
		# pass through each question
		for question in question_dicts:
			# question string stored in 'name' key
			questions.append(question['name'])

			# shuffle the answer keys list
			random.shuffle(answer_keys)
			# temporary list to hold answers for this question
			answers_temp = []
			# pass through each answer key
			for i, key in enumerate(answer_keys):
				# store answer in temporary list
				answers_temp.append(question[key]['name'])

				# if this is the correct answer, store index
				if key == 'correct':
					correct_indices.append(i)

			# store temporary list in answers list
			answers.append(answers_temp)

		return questions, answers, correct_indices

	def get_random_quiz(self):
		'''
		This returns a list of questions, a list of answers, and a list of correct indices. \
		These correspond to a random quiz where ten questions are taken at random from all sections.
		'''

		# get all questions from each section
		question_dicts = self.get_all_questions_dicts()
		# randomly shuffle
		random.shuffle(question_dicts)
		# now only take first 10 elements (shuffled so random order for first 10)
		question_dicts = question_dicts[:10]

		return self.process_question_dicts(question_dicts)

	def get_section_quiz(self, section):
		'''
		This returns a list of questions, a list of answers, and a list of correct indices. \
		These correspond to a section quiz where the name string of the section is supplied.
		'''

		# get all questions from each section
		question_dicts = self.get_questions_from_section(section)
		# randomly shuffle
		random.shuffle(question_dicts)

		return self.process_question_dicts(question_dicts)

if __name__ == '__main__':
	quiz = Quiz('assets/data/ClinicalPracticeWorkbook.txt')
	print(quiz.get_section_key_by_name('Chapter 2'))