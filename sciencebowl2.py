# modules for 
import PyPDF2
import os
from random import *
from progress.bar import *
from time import *

class Question(object):
	def __init__(self, question=None, answer=None, answers=[], science=None):
		self.question = question
		self.science = science
		self.answer = answer
		self.answers = answers

questions = []
pdfs = [0]
pages = [0]
start_time = [0]
questions_per_second = []
our_questions = []

total = [0]
correct = [0]

sciences = ["chemistry", "biology", "physics", "energy", "math", "earth and space"]

we_want = ["chemistry", "physics"]

types = ["multiple choice", "short answer"]

# finds the type of a question
def find_type(question)->"science":
	for science in sciences:
		if science.lower() in question.lower():
			return science

# splits and joins a string together
def joining(string, splitting)->str:
	for c in splitting:
		string = "".join(string.split(c))

	return string

# removes whitespace from a list
def whitespace(lst)->[]:
	return [item.strip() for item in lst]

# adds a question to the list
def addquestion(string)->bool:

	# finds the type, science, question and answers of the question

	string = string.lower().strip()

	stringscience = find_type(string)

	# if it is multiple choice
	if "multiple choice" in string:
		stringtype = "multiple choice"

	else:
		stringtype = "short answer"

	# find the answer
	stringanswer = string.split("answer:")[1].strip().split("toss")[0]

	# make an object
	stringobj = Question(answer=stringanswer, science=stringscience)

	# finds the question and answers, adds the entire question
	if stringtype == "multiple choice":

		# finds the question and answer
		stringquestion = string.split("multiple choice")[1].split("w) ")[0].strip()
		
		# updates the object
		stringobj.answers = whitespace([string.split("w)")[1].split("x)")[0].strip(), string.split("x)")[1].split("y)")[0].strip(),\
							 string.split("y)")[1].split("z)")[0].strip(), string.split("z)")[1].split("answer:")[0].strip()])

	else:
		# same process for short answer
		stringquestion = string.split("answer:")[0].split("short answer")[1].strip()

	# updates the object
	stringobj.question = stringquestion.capitalize()

	# adds it to the list

	if stringobj not in questions:
		questions.append(stringobj)

	return True

# makes a function to find questions of a certain type
def retrieve(science)->"matches":

	matches = []

	# for every question
	for question in questions:
		# if it matches
		if question.science == science:
			# add it
			matches.append(question)

	return matches

# parses the pdfs and adds the question
def parse(page)->bool:

	# retrieve and add the first one
	try:
		addquestion(page.split("TOSS-UP")[1].split("BONUS")[0])

	except:

		try:
			addquestion(page.split("TOSSUP")[1].split("BONUS")[0])

		except:
			pass

	# do the same for the second
	try:
		addquestion(page.split("BONUS")[1].split("TOSS-UP")[0])

	except:

		try:
			addquestion(page.split("BONUS")[1].split("TOSSUP")[0])
		
		except:
			pass

	try:

		addquestion(page.split("TOSS-UP")[2].split("BONUS")[0])

	except:

		try:
			addquestion(page.split("TOSSUP")[2].split("BONUS")[0])

		except:
			pass

	try:
		addquestion(page.split("BONUS")[2])
	
	except:
		pass

	return True

# finds the average questions per second
def avgQuestionsPerSecond()->int:

	return floor_num(sum(questions_per_second)/len(questions_per_second))

# print stats to the screen as the parsing runs
def print_stats()->bool:

	os.system("clear")			

	if not too_early():

		questions_per_second.append(questionsPerSecond())

		print("Time taken: %s seconds\n\nDocuments opened: %s\nPages parsed: %s\n\nQuestions found: %s\n\nQuestions per second: %s\nAverage questions per second: %s\n\nQuestions remaining: %s\nPercentage of questions parsed: %s\n\nTotal estimated time: %s seconds\nEstimated percentage of time elapsed: %s\nEstimated time to completion: %s seconds" %\
			(time_taken(), num_pdfs(), num_pages(), num_parsed(), questionsPerSecond(), avgQuestionsPerSecond(), questionsRemaining(), pct_questions(), total_time(), pct_time(), timeToCompletion()))

	else:
		pass

	return True

# searches the pdfs, parses it, and adds the questions to lists
def search()->bool:

	os.system("clear")

	# makes a bar
	# bar = ChargingBar("Progress: ", max=len(os.listdir(os.fsencode("Rounds/").decode())))

	# checks the time before starting
	start_time[0] = time()

	# for every pdf
	for file in os.listdir(os.fsencode("Rounds/").decode()):

		# bar.next()

		# pdf reader object
		pdfReader = PyPDF2.PdfFileReader(open("Rounds/%s" % os.fsdecode(file), "rb"))

		pdfs[0] += 1

		# for every page
		for _ in range(pdfReader.numPages):

			print_stats()

			pages[0] += 1

			page = pdfReader.getPage(_).extractText().strip()
			# get rid of useless characters
			page = joining(page, ["\n", "~~~~", "~~", "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~", "™", "¿", "é",\
								 "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~", "Œ", "ð", "õ", "Õ",\
								  "________________________________________________________________________",\
								   "_______________________________________________________"])

			# parse the page
			parse(page)

	# bar.finish()

	shuffle(questions)

	os.system("clear")

	return True

# makes a function that deals with multiple choice question answers
def wxyz(question)->"answers":

	answers = []

	# adds the letter to each answer
	for i, c in enumerate(["w", "x", "y", "z"]):
		answers.append("%s) %s" % (c, question.answers[i]))

	return answers

# makes a function to format the question
def format(question)->str:

	# if it is short answer
	if question.answers == []:
		# format the question
		return "%s   Short Answer\n\n%s\n\nAnswer: %s\n\n\n" %\
		(question.science.capitalize(), question.question.capitalize(), question.answer.capitalize())

	# format the multiple choice
	return "%s   Multiple Choice\n\n%s\n\n%s\n%s\n%s\n%s\n\nAnswer: %s\n\n\n" %\
			(question.science.capitalize(), question.question.capitalize(),\
			wxyz(question)[0].capitalize(),  wxyz(question)[1].capitalize(),\
			wxyz(question)[2].capitalize(),  wxyz(question)[3].capitalize(),\
			question.answer.capitalize())

# return the filename given a science
def fname(science)->"filename":
	return "Questions/%s.txt" % "_".join(science.split())

# writes to the file
def write()->bool:
	# for every science
	for science in sciences:
		try:
			# try to make a file
			with open(fname(science), "x") as file:
				pass
		except:
			# if it already exists
			with open(fname(science), "w") as file:

				# open it

				# for every question of that type
				for question in retrieve(science):
					# write the question
					file.write(format(question))

	return True

# returns the number of questions parsed
def num_parsed()->int:
	return len(questions)

# returns the total number of pages
def num_pages()->int:
	return pages[0]

# returns the number of pdfs found
def num_pdfs()->int:
	return pdfs[0]

# returns the time taken
def time_taken(places=0)->int:
	return floor_num(time() - start_time[0], places)

# returns the questions answered per second
def questionsPerSecond()->int:
	return floor_num(num_parsed()/time_taken())

# returns the questions remaining
def questionsRemaining(total=9634):
	return total - num_parsed()

# helps with decimal places
def floor_num(integer, places=0)->int:
	# looks through indexes and characters of the string
	for i, c in enumerate(str(integer)):
		# if we find the decimal
		if c == ".":
			# modify it so we can splice out the wanted decimal places
			splicingIndex = i + places

			return int(str(integer)[:splicingIndex])

# returns the estimated amount of time to completion
def timeToCompletion()->int:

	return floor_num(questionsRemaining()/avgQuestionsPerSecond())

# returns the total estimated time
def total_time()->int:
	return time_taken() + timeToCompletion()

# returns the percentage of time elapsed
def pct_time()->int:
	return str(floor_num(100 * time_taken()/total_time())) + " %"

# returns the percentage of questions parsed
def pct_questions(total=9634):
	return str(floor_num(100 * num_parsed()/total)) + " %"

# give the results
def give_results(calculations=True)->bool:

	# if there is an 
	if not calculations:
		input("\nSuccessfully parsed 0 questions\nSearched %s pages of %s documents\nTook %s seconds (0 questions per second)\nPress enter to continue."\
				% (num_pages(), num_pdfs(), time_taken()))

	else:
		input("Successfully parsed %s questions\nSearched %s pages of %s documents\nTook %s seconds (~%s questions per second)\nPress enter to continue."\
				% (num_parsed(), num_pages(), num_pdfs(), time_taken(), avgQuestionsPerSecond()))	

	return True

# defines if it is too early to do calculations
def too_early()->bool:
	return len(questions) == 0 or time_taken() == 0

# stop the program if there is an error
def stop(results=True):

	if results:
		try:
			if too_early():
				give_results(calculations=False)
			
			else:
				give_results()

		except:
			pass

	print("\nQuitting program...")
	quit()

# prints an error
def error(string)->bool:
	input(string + ".\nPress enter to continue.")

# displays info
def display(string="")->bool:
	input(string + "\nPress enter to continue.")

# decides if the user wants to continue
def prompt_continue()->bool:

	usr = ""

	while usr == "":

		os.system("clear")

		usr = input("Do you want to continue (y/n) ? ")

		if len(usr) == 0:
			usr = ""
			error("You must enter something")
			continue

		if len(usr) != 1 or usr.lower() not in ["y", "n"]:
			usr = ""
			error('You must enter either "y" or "n"')
			continue

	if usr == "n":
		display("\nYour response: No")

		stop(results=False)

	else:
		display("\nYour response: Yes")

	return True

# asks the question
def ask(question)->"answer":

	answer = ""

	while answer == "":

		os.system("clear")

		if total[0] != 0:
			string = "Questions answered: %s\nQuestions correct: %s\nPercentage correct: %s" % (total[0], correct[0], floor_num(100 * correct[0]/total[0]))
			string += "%"
			string += "\n\n"
			print(string)

		# if it is short answer
		if question.answers == []:
			usr = input("%s   Short Answer\n\n%s\n\nAnswer: " % (question.science.capitalize(), question.question))

			return usr.lower()

		usr = input("%s   Multiple Choice\n\n%s\n\n%s\n%s\n%s\n%s\n\nAnswer: " %\
				(question.science.capitalize(), question.question,\
				question.answers[0].capitalize(), question.answers[1].capitalize(),\
				question.answers[2].capitalize(), question.answers[3].capitalize()))


		return usr.lower()

# returns a lsit of the answers properly formatted
def format_answers(answers):
	new_answers = []

	# loop through each answer
	for i, answer in enumerate(answers):

		# if there is no letter already
		if ["w", "x", "y", "z"][i] not in answer[:3]:
			new_answers.append("%s) %s" % (["w", "x", "y", "z"][i], answer))

	return new_answers

# finds questions of our type
def find_questions()->bool:

	# for every science
	for science in we_want:
		# for every question of that science
		for question in retrieve(science):

			# if it is short answer and we want short answer
			if question.answers == [] and "short answer" in types:
				# add it
				our_questions.append(question)
			# if we want multiple choice
			elif "multiple choice" in types and len(question.answers) == 4:

				# remove the letter and parentheses from the answer
				new_question = Question(question=question.question.strip(), answer=question.answer[3:].strip(),\
										 answers=format_answers(question.answers),\
										 science=question.science.strip())

				our_questions.append(new_question)

	shuffle(our_questions)

	return True

# finds the first letter (w, x, y, or z) of an answer given the list
def answer_first_letter(answer, answers):

	# for every answer
	for option in format_answers(answers):
		if answer in option:
			return option[0]


# returns the option given a letter

def option_given_letter(letter, answers):

	# for every letter
	for i, c in enumerate(["w", "x", "y", "z"]):
		# if the user entered it
		if c == letter:
			# save it
			answer = answers[i]
			break

	# loop through the list again to get rid of the letters
	for c in ["w", "x", "y", "z"]:
		answer = "".join(answer.split("%s) " % c))

	return answer

# checks to see if the user is right, and gives them the result
def check(answer, usr, answers)->bool:

	if usr == "":
		display('\nIncorrect! The correct answer was "%s"' % answer)
		return False

	# if it is short answer
	if answers == []:

		# if they got it fully correct
		if usr == answer:
			display('\nCorrect! You correctly entered "%s"' % usr)
			return True

		# if they got it partially correct
		if usr in answer:
			display('\nPartially correct! You entered "%s", but the correct answer was "%s"' % (usr, answer))
			return True

		# if they got it wrong
		else:
			display('\nIncorrect! You entered "%s", but the correct answer was "%s"' % (usr, answer))
			return False

	# if it is multiple choice

	# if they got it fully correct
	if usr == answer_first_letter(answer, answers):
		display('\nCorrect! You correctly entered "%s) %s"' % (usr.upper(), answer))
		return True

	# if they got it wrong
	else:
		display('\nIncorrect! You entered "%s) %s", but the correct answer was "%s) %s"'\
				% (usr.upper(), option_given_letter(usr, answers), answer_first_letter(answer, answers).upper(), answer))

		return False

# updates the number of questions answered
def update_question_num()->bool:
	total[0] += 1
	return True

# updates the number of correct questions


# runs the program
def run()->bool:
	try:
		search()
		write()
		give_results()

		prompt_continue()

		find_questions()

		for question in our_questions:

			# if it has the right number of answers
			if len(question.answers) in [0, 4]:

				usr_answer = ask(question)

				# if they got it right
				if check(question.answer, usr_answer, format_answers(question.answers)):
					correct[0] += 1

				update_question_num()

	except KeyboardInterrupt:
		stop(results=False)

	return True

try:
	search()
	write()
	give_results()

	prompt_continue()

	find_questions()

	for question in our_questions:

		# if it has the right number of answers
		if len(question.answers) in [0, 4]:

			usr_answer = ask(question)

			# if they got it right
			if check(question.answer, usr_answer, format_answers(question.answers)):
				correct[0] += 1

			update_question_num()

except KeyboardInterrupt:
	stop(results=False)