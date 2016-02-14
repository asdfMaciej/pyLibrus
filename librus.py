from bs4 import BeautifulSoup
import pickle
import requests
import time


class GradeBook:
	"""GradeBook - Stores grades. Allows sorting and displaying all at once.

	Variables:
	grades (list) - The list of grades.
	subjects (list) - The list of school subjects.
	grades_id (list) - The list of grades' IDs.
	dates (list) - The list of grades' dates.
	teachers (dictionary) - A dictionary of teachers.
		{subject:teacher}
	subject_grades (dictionary) - A list of grades per subject.
		{subject:[grades]}
	midterm_grades (dictionary) - A list of midterm grades per subject.
		{subject:[grades]}
	old_grades (GradeBook) - The GradeBook used on last launch.
		Set upon calling update_old_grades().
	librus (Librus) - Reference to the parent Librus object.
		Set in Librus object during init.

	Functions:
	add(grade) - Add a grade into the GradeBook.
	display() - Return the grades from the GradeBook, allowing to display them.
	sort_by_weight(reverse=False) - Sort the grades by their weight.
	sort_by_date(reverse=False) - Sort the grades by their date.
	sort_by_grade(reverse=False) - Sort the grades by their value.
	calculate_average(subject) - Calculate average of a specified subject,
		taking weights in account.
	update_old_grades() - Update old_grades with grades from last launch.
	compare_old_grades() - Compare old_grades with grades, returns new ones.
		Returns a GradeBook object.
	"""
	def __init__(self):
		"""Initializes the GradeBook by initializing variables."""
		self.grades = []
		self.grades_id = []
		self.dates = []
		self.subjects = []
		self.teachers = {}
		self.subject_grades = {}
		self.midterm_grades = {}
		self.old_grades = None
		self.librus = None

	def add(self, grade):
		"""add(grade) - Add a grade into the GradeBook.

		Parameters:
		grade - a Grade() object.
		"""
		self.grades.append(grade)
		if grade[3] not in self.subjects:  # grade[3] is the school subject
			self.subjects.append(grade[3])
			self.subject_grades[grade[3]] = []
			self.midterm_grades[grade[3]] = []

		if grade[9] not in self.teachers:
			self.teachers[grade[3]] = grade[9]  # {subject:teacher}

		if grade[1] == 1:  # If grade numtype equals MidtermGrade
			if "śródroczna" in grade[7]:  # If śródroczna is in description
				self.midterm_grades[grade[3]].append(grade)

		if grade[0] not in self.grades_id:  # grade[0] is the id in librus
			self.grades_id.append(grade[0])

		if grade[5] not in self.dates:  # grade[5] is the date
			self.dates.append(grade[5])

		self.subject_grades[grade[3]].append(grade)

	def update_old_grades(self):
		"""update_old_grades() - Updates old_grades with grades
		from last launch. Filename used: grades_old.pickle 
		"""
		filename = 'grades_old.pickle'
		temp_old_grades = self.librus.file_handler.file_to_class(filename)
		self.old_grades = GradeBook()
		for grade in temp_old_grades.grades:
			self.old_grades.add(grade)

		self.old_grades.sort_by_date()

	def compare_old_grades(self):
		"""compare_old_grades() - Compares old_grades with grades,
		returns new ones. Returns a GradeBook object.
		"""
		temp_gradebook = GradeBook()
		for grade in self.grades:
			if str(grade.grade_id) not in self.old_grades.grades_id:
				temp_gradebook.add(grade)
			elif str(grade.date) not in self.old_grades.dates:
				temp_grade_book.add(grade)

		return temp_gradebook

	def display(self):
		"""display() - Return the grades from the GradeBook,
		allowing to display them.
		"""
		display_text = ""
		for grade in self.grades:
			display_text += grade.display()

		if not self.grades:
			display_text = "No grades found."

		return display_text

	def sort_by_weight(self, reverse=False):
		"""sort_by_weight(reverse=False) - Sort the grades by their weight.

		Keyword parameters:
		reverse (bool) - whether to reverse the list or not. (default False)
		"""
		self.grades.sort(key=lambda x: int(x[8]), reverse=reverse)

	def sort_by_date(self, reverse=False):
		"""sort_by_date(reverse=False) - Sort the grades by their date.

		Keyword parameters:
		reverse (bool) - whether to reverse the list or not. (default False)
		"""
		self.grades.sort(key=lambda x: str(x[5]), reverse=reverse)

	def sort_by_grade(self, reverse=False):
		"""sort_by_grade(reverse=False) - Sort the grades by their value.

		Keyword parameters:
		reverse (bool) - whether to reverse the list or not. (default False)
		"""
		self.grades.sort(key=lambda x: int(x[13]), reverse=reverse)

	def calculate_average(self, subject):
		"""calculate_average(subject) -
		Calculates an average of a specified subject, taking weights in account.

		Parameters:
		subject (string) - The mentioned subject.
		"""
		if subject not in self.subjects:
			raise NameError(
				'Subject not found - ' + subject +
				'. Use ones specified in GradeBook.subjects next time.'
			)

		temp_grades = []
		temp_sum = 0
		temp_count = 0
		for x in self.subject_grades[subject]:
			if x.absolute_value and (x.calculate_towards_avg_grade == 1):
				temp_grades.append(x)

		for x in temp_grades:
			temp_sum += x.absolute_value * x.weight
			temp_count += x.weight

		return float(temp_sum/temp_count)


class EventCalendar:
	"""EventCalendar - Stores events. Allows displaying all of them at once.

	Variables:
	events (list) - The list of events.
	events_id (list) - The list of events' IDs.
	events_day (list) - The list of events' days.
	old_events (EventCalendar) - The EventCalendar used on last launch.
	librus (Librus) - Reference to the parent Librus object.
		Set in Librus object during init.

	Functions:
	add(event) - Add an event into the EventCalendar.
	display() - Return the events from the EventCalendar,
		allowing to display them.
	update_old_events(month, year) - Update the old_events with ones
		stored in events<month>_<year>_old.pickle.
	compare_old_events() - Compare the old_events with events and
		returns the new added ones. Returns an EventCalendar.
	sort_by_day(reverse) - Sort the events by their day.
	"""
	def __init__(self):
		"""Initializes the EventCalendar by initializing variables."""
		self.events = []
		self.events_id = []
		self.events_day = []
		self.old_events = None
		self.librus = None

	def add(self, event):
		"""add(event) - Add an event into the EventCalendar.

		Parameters:
		event - a Event() object.
		"""
		self.events.append(event)
		if event[10] not in self.events_id:  # id
			self.events_id.append(event[10])
		if event[4] not in self.events_day:  # day
			self.events_day.append(event[4])

	def update_old_events(self, month, year):
		"""update_old_events(month, year) - Update the old_events with ones
		stored in events<month>_<year>_old.pickle.

		Parameters:
		month (string) - The desired month.
		year (string) - The desired year.
		"""
		filename = 'events'+str(month)+'_'+str(year)+'_old.pickle'
		temp_old_events = self.librus.file_handler.file_to_class(filename)
		self.old_events = EventCalendar()
		for event in temp_old_events.events:
			self.old_events.add(event)

	def compare_old_events(self):
		"""compare_old_events() - Compare the old_events with events and
		returns the new added ones. Returns an EventCalendar.
		"""
		temp_event_calendar = EventCalendar()
		for event in self.events:
			if str(event.event_id) not in self.old_events.events_id:
				temp_event_calendar.add(event)
			# elif str(event.day) not in self.old_events.events_day:
			# temp_event_calendar.add(event)

		return temp_event_calendar

	def display(self):
		"""display() - Return the events from the EventCalendar,
		allowing to display them.
		"""
		display_text = ""
		for event in self.events:
			display_text += event.display()
		return display_text

	def sort_by_day(self, reverse=False):
		"""sort_by_day(reverse=False) - Sort the events by their day.

		Keyword parameters:
		reverse (bool) - whether to reverse the list or not. (default False)
		"""
		temp_events = []
		for event in self.events:
			if not (len(event.values[4]) - 1):
				event.values[4] = str('0'+str(event.values[4]))
			temp_events.append(event)
		self.events = temp_events
		self.events.sort(key=lambda x: str(x[4]), reverse=reverse)


class Grade:
	"""Grade - A grade object. Stores all of values,
	allows displaying it on a function call.

	Variables:
	values (list) - Provided by Parser class, a list of values:
		[0] - grade_id
		[1] - grade_numtype
		[2] - grade_type
		[3] - school_subject
		[4] - grade_value
		[5] - date
		[6] - day_of_the_week
		[7] - category
		[8] - weight
		[9] - teacher
		[10] - calculate_towards_avg_grade
		[11] - added
		[12] - description
		Added upon initialization to the list:
		[13] - absolute_value
	grade_numtype (int) - Type of the grade:
		0 - DescriptiveGrade - Doesn't have weight (-1) and doesn't specify
		calculating towards avg grade (-1). Sometimes has a description.
		1 - MidtermGrade - Doesn't have weight (-1), doesn't calculate
		towards avg grade. (0)
		2 - StandardGrade - Has weight and can calculate
		towards average grade. (doesn't have to)
		3 - ShapingGrade - Doesn't have weight and doesn't specify
		calculating towards avg grade, always has a description.
	grade_id (int) - ID of grade in Librus.
	grade_type (string) - Type of the grade, corresponds to grade_numtype.
	grade_value (string) - The grade itself.
	absolute_value (int) - A numerical representation of the grade.
	(without the +/- at end or T/np)
	school_subject (string) - School subject of the grade.
	date (string) - Date in which the grade was written. YYYY-MM-DD
	day_of_the_week (string) - Day of the week in which the grade
	was written. (pon./wt./śr./czw./pt.)
	category (string) - Type/category of the grade, for ex. exam/vocal exam.
	weight (int) - Weight of the grade. If no data specified, -1.
	teacher (string) - Teacher who teaches the subject.
	added (string) - Teacher who added the grade
	(usually the same as var teacher)
	calculate_towards_avg_grade (int) - Whether the grade calculates
	to average or not. Either 0 or 1. If no data specified, -1.
	description (string) - Description of the grade.

	Functions:
	__init__(values) - Accepts the values from Parser.parse_grade and
	puts them into array. Initializing method.
	update(values) - Updates the values with new ones. Done on initialization.
	display() - Returns a text representation of the grade,
	which can be used for display.
	set_absolute_values() - Turns the grade_value into absolute_value.
	Done on initialization.
	return_values() - Returns the internal list of values.
	"""

	def __init__(self, values):
		"""Initializes the Grade by initializing variables, updating them
			and creating a numeral representation of the grade.

		Parameters:
		values (list) - A list of values, provided by Parser.parse_grade.
		"""
		self.values = []
		self.grade_id = 0
		self.grade_numtype = 0
		self.grade_type = ""
		self.school_subject = ""
		self.grade_value = ""
		self.absolute_value = 0
		self.date = ""
		self.day_of_the_week = ""
		self.category = ""
		self.weight = 0
		self.teacher = ""
		self.calculate_towards_avg_grade = 0
		self.added = ""
		self.description = ""

		self.update(values)
		self.set_absolute_values()
		self.values.append(self.absolute_value)  # values[13]

	def __getitem__(self, index):
		"""Allows sorting with .sort()."""
		return self.values[index]

	def __str__(self):
		"""Allows printing the Grade in a str() manner."""
		return self.display()

	def update(self, values):
		"""update(values) - Updates the variables in Grade class with
		ones provided in arguments. Called on initialization.

		Parameters:
		values (list) - A list of values, provided by Parser.parse_grade.
		"""
		self.values = values

		self.grade_id = int(values[0])
		self.grade_numtype = int(values[1])
		self.grade_type = values[2]
		self.school_subject = values[3]
		self.grade_value = values[4]
		self.date = values[5]
		self.day_of_the_week = values[6]
		self.category = values[7]
		self.weight = int(values[8])
		self.teacher = values[9]
		self.calculate_towards_avg_grade = int(values[10])
		self.added = values[11]
		self.description = values[12]
		# self.absolute_value = values[13]

	def display(self):
		"""display() - Returns a text representation of the grade,
		which can be used for display.
		"""
		display_string = "["
		display_string += self.date + ", " + self.day_of_the_week + "] - <"
		display_string += self.school_subject + "> (" + self.grade_value + ")"
		if self.weight != -1:
			display_string += " - Waga: " + str(self.weight)
		if self.calculate_towards_avg_grade != -1:
			display_string += ". Liczy się: "
			display_string += {0: "Nie", 1: "Tak"}[self.calculate_towards_avg_grade]
		display_string += ". Typ oceny: " + self.category
		display_string += ". Dodał/a " + self.teacher + ", id w Librusie: "
		display_string += str(self.grade_id) + "."
		if self.description:
			display_string += " Opis: "+self.description
		display_string += "\n"
		return display_string

	def set_absolute_values(self):
		"""set_absolute_values() - Turns the grade_value into absolute_value.
		Called on initialization
		"""
		if self.grade_value in ("-", "+", "T", "np"):
			self.absolute_value = 0
		else:
			if len(self.grade_value) > 1:
				if "+" == self.grade_value[1]:
					self.absolute_value = float(self.grade_value[0])
					self.absolute_value += 0.5
				elif "-" == self.grade_value[1]:
					self.absolute_value = float(self.grade_value[0])
					self.absolute_value -= 0.25
			else:
				self.absolute_value = int(self.grade_value)

	def return_values(self):
		"""return_values() - Returns the internal list of values."""
		return self.values


class Event:
	"""Event - An event object. Stores events and all of their data.
	Allows displaying it with a function call.

	Description:
	"if it ain't broke, don't fix it"

	Variables:
	values (list) - provided by Parser class, a list of values:
		[0] - description_additional
		[1] - date
		[2] - teacher
		[3] - absence_period
		[4] - day
		[5] - month
		[6] - year
		[7] - event_type
		[8] - event_numtype
		[9] - description
		[10] - event_id
	event_numtype (int) - type of the Event:
		0 - Holiday
		1 - Absence [as in teacher]
		2 - Parent-teacher meeting
		3 - Substitute [as in teacher]
		4 - Exam
		5 - Test
		6 - Lesson observation
	event_type (str) - type of the Event, corresponds to event_numtype:
		Dzień wolny, (0)
		Nieobecność, (1)
		Wywiadówka, (2)
		Zastępstwo, (3)
		Sprawdzian, (4)
		Kartkówka, (5)
		Obserwacja lekcji (6)
	date (str) - date in which the event was inputed in Librus
	teacher (str) - teacher in mentioned event. Works in numtypes
		1, 2, 3, 4, 5, 6.
		In 1, it's the absent teacher.
		In 2, it's the class teacher, which put the event in Librus.
		In 3, it's the teacher who is a Substitute.
		In 4-6, it's the lesson teacher.
	absence_period (str) - lesson number of a given event or the
		absence period of a teacher, for ex. (4 do 6)
		Works on numtypes 4, 5, 6 and sometimes 1.
		4, 5, 6 - the lesson number of the event.
		1 - the lesson numbers the teacher won't be in school, assuming
		the absence is only partial [not full day]. If it's a full day,
		absence_period will be "".
	day (int) - day of the event
	month (str) - month of the event, in Polish. for ex. Październik
	year (int) - year of the event
	description (str) - description of the event, on numtypes 4/5/6
	description_additional (str) - additional description
	event_id (int) - id of event in librus. Defaults to 0 when couldn't be found

	Functions:
	__init__(values) - Accepts the values from Parser.parse_events and
	puts them into an array. Initializing method.
	update(values) - Updates the values with new ones. Done on initialization.
	display() - Returns a text representation of the event,
	which can be used for display.
	"""
	def __init__(self, values):
		"""__init__(values) - Accepts the values from Parser.parse_events and
		puts them into an array. Initializing method.

		Parameters:
		values (list) - The list of values, provided by Parser.parse_events
		"""
		self.values = []

		self.description_additional = ""
		self.date = ""
		self.teacher = ""
		self.absence_period = ""
		self.day = 0
		self.month = ""
		self.year = 0
		self.event_type = ""
		self.event_numtype = 0
		self.description = ""
		self.event_id = 0

		self.update(values)

	def __getitem__(self, index):
		"""Allows sorting with .sort()."""
		return self.values[index]

	def __str__(self):
		"""Allows printing the Event in a str() manner."""
		return self.display()

	def update(self, values):
		"""update(values) - Updates the values with new ones.
		Called on initialization.

		Parameters:
		values (list) - The list of values, provided by Parser.parse_events
		"""
		self.values = values

		self.description_additional = values[0]
		self.date = values[1]
		self.teacher = values[2]
		self.absence_period = values[3]
		self.day = int(values[4])
		self.month = values[5]
		self.year = int(values[6])
		self.event_type = values[7]
		self.event_numtype = int(values[8])
		self.description = values[9]
		self.event_id = int(values[10])

	def display(self):
		"""display() - Returns a text representation of the event,
		which can be used for display.
		"""
		temp_date = str(self.day) + ", " + str(self.month) + " " + str(self.year)
		if self.event_numtype == 0:  # Dni wolne
			display_string = "["+temp_date+"]"+": "+self.event_type+" - "
			display_string += self.description_additional
		elif self.event_numtype in (2, 4, 5):  # Kartkowki, sprawdziany i wywiadowki
			display_string = "["+temp_date+"]"+": "+self.event_type + " z "+self.teacher
			if self.event_numtype != 2:
				display_string += " na lekcji nr. "+self.absence_period
			display_string += ": " + self.description
		elif self.event_numtype == 1:  # Nieobecnosci
			display_string = "["+temp_date+"]: " + self.event_type+" - "+self.teacher
			if self.absence_period:
				display_string += ", od lekcji "+self.absence_period+"."
		elif self.event_numtype == 3:  # zastepstwa
			display_string = "["+temp_date+"]: "+self.event_type+" z "+self.teacher
			display_string += " na lekcji nr. "+self.date+" - "
			display_string += self.description_additional
		elif self.event_numtype == 6:  # obserwacje lekcji
			display_string = "["+temp_date+"]: "+self.event_type+" - "+self.description
		display_string += "\n"
		return display_string


class Parser:
	"""Parser - a parser object, used to parse HTML into variables.

	Variables:
	librus (Librus) - Reference to the parent Librus object.
		Set in Librus object during init.

	Functions:
	parse_grade(grade) - Parses BeautifulSoup grades provided by
	Parser.parse_html_grade. Returns a list of values.
	parse_events(events, html) - Parses HTML and BeautifulSoup events provided by
	Parser.parse_html_table, returns a list of values.
	parse_html_grade(html) - Parses HTML into BeautifulSoup grades.
	parse_html_table(html) - Parses HTML into BeautifulSoup events.
	"""
	def __init__(self):
		self.librus = None

	def parse_grade(self, grade):
		"""parse_grade(grade) - Parses a grade object provided by BeautifulSoup
		[don't confuse with the class Grade]. Returns a list of values.

		Parameters:
		grade (object) - provided by Parser.parse_html_grade.
		"""
		school_subject = repr(grade.findParents('tr')[0])
		school_subject = school_subject.split('/tree_colapsed.png"/>')[1]
		school_subject = school_subject.split('<td>')[1].split('</td>')[0]
		grade_id = repr(grade).split("szczegoly/")[1].split('" title')[0]
		grade_value = str(grade.text)
		category = repr(grade).split("Kategoria: ")[1].split('&lt;')[0]
		date = repr(grade).split("Data: ")[1].split('&lt;')[0].split(' (')[0]
		day_of_the_week = repr(grade).split("Data: ")[1].split('&lt;')[0]
		day_of_the_week = day_of_the_week.split(' (')[1].split(')')[0]
		teacher = repr(grade).split('Nauczyciel: ')[1].split('&lt;')[0]
		added = repr(grade).split('Dodał: ')[1].split('&lt;')[0]

		try:
			temp_types = {'tak': True, 'nie': False}
			calculate_towards_avg_grade = repr(grade).split('średniej: ')
			calculate_towards_avg_grade = calculate_towards_avg_grade[1].split('&lt;')
			calculate_towards_avg_grade = temp_types[calculate_towards_avg_grade[0]]
			has_average = True
		except:
			calculate_towards_avg_grade = -1
			has_average = False

		try:
			weight = repr(grade).split('Waga: ')[1].split('&lt;')[0]
			has_weight = True
		except:
			weight = -1
			has_weight = False

		if 'ksztaltujace' in grade_id:
			grade_id = grade_id.split('ksztaltujace/')[1]
			grade_type = "ShapingGrade"
			grade_numtype = 3
		else:
			temp_types = {0: "DescriptiveGrade", 1: "MidtermGrade", 2: "StandardGrade"}
			grade_numtype = has_weight + has_average
			grade_type = temp_types[grade_numtype]

		try:
			description = repr(grade).split('Ocena: ')[1].split('&lt;')[0]
		except:
			description = ""

		return [
				grade_id, grade_numtype, grade_type, school_subject, grade_value, date,
				day_of_the_week, category, weight, teacher,
				calculate_towards_avg_grade, added, description
		]

	def parse_events(self, events, html):
		"""parse_events(events, html) - parses HTML and BeautifulSoup events
		provided by Parser.parse_html_table and returns a list of values.

		Parameters:
		events (object) - provided by Parser.parse_html_table.
		html (string) - the HTML of events webpage.
		"""
		events_list = []
		parsed_html = events
		td_list = []
		types_dict = {
			'style="background-color: #FF7878; cursor: pointer;"': 0,  # dni wolne
			'style="background-color: #FF7878; "': 1,  # nieobecnosci
			'style="background-color: #abcdef; "': 2,  # wywiadowki
			'style="background-color: #6A9604; "': 3,  # zastepstwa
			'style="background-color: #DC143C; cursor: pointer;"': 4,  # sprawdziany
			'style="background-color: #FF8C00; cursor: pointer;"': 5,  # kartkowki
			'style="background-color: #BA55D3; cursor: pointer;"': 6   # obserwacje
		}
		types_dict_string = {
			0: "Dzień wolny",
			1: "Nieobecność",
			2: "Wywiadówka",
			3: "Zastępstwo",
			4: "Sprawdzian",
			5: "Kartkówka",
			6: "Obserwacja lekcji"
		}
		dodane_id = {}

		for div in parsed_html:
			td_list.append(div.find_all('td'))

		for i in range(len(td_list)):
			for td in td_list[i]:
				tekst = repr(td.parent.parent.parent.parent)
				if '</tr>' not in repr(tekst):
					continue
				for temp_event in repr(tekst).split('</tr>'):
					absence_period = ""
					event_numtype = 0
					month = html.split('selected="selected" >')[1].split('</')[0]
					day = tekst.split('numer-dnia">')[1].split('</div>')[0]
					year = html.split('selected="selected" > ')[1].split('</')[0]
					if 'szczegoly_wolne' in temp_event:
						event_id = temp_event.split('/szczegoly_wolne/')[1].split("'")[0][:-2]
					elif 'szczegoly' in temp_event:
						event_id = temp_event.split('terminarz/szczegoly/')[1].split("'")[0][:-2]
					else:
						event_id = 0

					temp_list = list(types_dict)
					temp_list.append("#6A9604")
					for abc in temp_list:
						if abc in temp_event:
							if abc != "#6A9604":
								event_numtype = types_dict[abc]
							else:
								event_numtype = 3
					event_type = types_dict_string[event_numtype]

					if event_numtype in (2, 4, 5, 6):
						teacher = temp_event.split('Nauczyciel: ')[1].split('&lt;')[0]
					else:
						teacher = ""

					if event_numtype in (5, 4, 2, 6):
						temp_desc = temp_event.split('&gt;Opis: ')[1].split('onclick')[0]
						temp_desc = '\n'.join(temp_desc.split('<br/>')[:-1])
						temp_desc = temp_desc.split('&lt;br /&gt;')[:-1]
						description = ' '.join(temp_desc)
						date = temp_event.split('Data dodania: ')[1].split('"')[0]
					else:
						description = ""
						date = ""

					if event_numtype in (0, 1, 2, 4, 5):
						try:
							if '</td>' in temp_event:
								temp_desc = temp_event.split('">')[-1].split("</td>")
								temp_desc = temp_desc[0].replace('<br/>', '\n')
								description_additional = temp_desc
						except:
							description_additional = ""
					else:
						description_additional = ""

					if event_numtype == 1:
						teacher = temp_event.split('Nauczyciel: ')[1].split('</td>')[0]
						if '<br/>' in teacher:
							teacher, absence_period = teacher.split('<br/>')
							absence_period = absence_period.split('lekcji: ')[1]
							absence_period = absence_period[:-1]  # removes trailing space
					else:
						absence_period = ""

					if event_numtype in (4, 5, 6):
						try:
							absence_period = description_additional.split('lekcji: ')[1]
							absence_period = absence_period.split(' ')[0]
						except:
							absence_period = ""

					if event_numtype == 3:
						teacher = temp_event.split('Zastępstwo z ')[1].split(' na')[0]
						date = temp_event.split('nr: ')[1].split(' (')[0]
						description_additional = temp_event.split('(')[1].split(')')[0]

					if description_additional not in dodane_id:
						dodane_id[description_additional] = [day]
						events_list.append(
							[
								description_additional, date, teacher,
								absence_period, day, month, year, event_type,
								event_numtype, description, event_id
							]
						)

					elif day not in dodane_id[description_additional]:
						dodane_id[description_additional].append(day)
						events_list.append(
							[
								description_additional, date, teacher,
								absence_period, day, month, year, event_type,
								event_numtype, description, event_id
							]
						)

		return events_list

	def parse_html_grade(self, html):
		"""parse_html_grade(html) - parses html and returns a list of soup grades
		(used in Parser.parse_grade)

		Parameters:
		html (string) - the HTML of grades website.
		"""
		soup = BeautifulSoup(html, "html.parser")
		soupGrades = soup.findAll("a", {"class": "ocena"})
		return soupGrades

	def parse_html_table(self, html):
		"""parse_html_table(html) - parses html and returns a list of soup tables
		(used in Parser.parse_event)

		Parameters:
		html (string) - the HTML of events website.
		"""
		soup = BeautifulSoup(html, "html.parser")
		soupGrades = soup.findAll("div", {"class": "kalendarz-dzien"})
		return soupGrades


class FileHandler:
	"""FileHandler - a file handler. Handles all of file related stuff.

	Variables:
	librus (Librus) - Reference to the parent Librus object.
		Set in Librus object during init.

	Functions:
	read_file(name, mode="r") - opens a file and returns its content.
	save_file(name, content, mode="w") - opens a file and writes into it.
	class_to_file(self, specified_class, name) - saves a class into a file.
	file_to_class(self, specified_class, name) - reads a class from a file.
	"""
	def __init__(self):
		self.librus = None

	def read_file(self, name, mode="r"):
		"""read_file(name) - opens a file and returns its content.

		Parameters:
		name (string) - the filename.

		Keyword parameters:
		mode (string) - the mode in which the file should be opened. (default r)
		"""
		tFile = open(name, mode, encoding="utf8")
		tContent = tFile.readlines()
		tFile.close()
		return "/n".join(tContent)

	def save_file(self, name, content, mode="w"):
		"""save_file(name, content, mode="w") - opens a file and writes into it.

		Parameters:
		name (string) - the filename.
		content (string) - the content which should be writed.

		Keyword parameters:
		mode (string) - the mode in which file should be opened. (default w)

		"""
		tFile = open(name, mode, encoding="utf8")
		tFile.write(content)
		tFile.close()
		return True

	def class_to_file(self, specified_class, name):
		"""class_to_file(self, specified_class, name) - saves a class into a file.
		Utilises the pickle module in order to save.

		Parameters:
		specified_class (object) - the class that should be saved
		name (string) - the filename
		"""
		temp_file = open(name, "wb")
		pickle.dump(specified_class, temp_file)
		temp_file.close()
		return True

	def file_to_class(self, name):
		"""file_to_class(self, specified_class, name) - reads a class from a file.
		Utilises the pickle module in order to read.

		Parameters:
		name (string) - the filename
		"""
		temp_file = open(name, "rb")
		temp_pickle = pickle.load(temp_file)
		temp_file.close()
		return temp_pickle


class LibrusFetcher:
	"""LibrusFetcher - a Librus web fetcher. Downloads the required webpages.

	Variables:
	url_grades (string) - the URL to grades page on Librus.
	url_events (string) - the URL to events page on Librus.
	url_login (string) - the URL to login page on Librus.
	headers (dictionary) - headers used in page request.
	payload (dictionary) - POST data used in initial login.
	cookies (dictionary) - cookies used in initial login.
	librus (Librus) - Reference to the parent Librus object.
		Set in Librus object during init.

	Functions:
	fetch_grades(login, password) - fetches the grades and returns the HTML.
	fetch_events(login, password, month, year) - fetches events
		and returns the HTML.
	"""
	def __init__(self):
		"""__init__() - Initialize the class by declaring variables."""
		self.librus = None
		self.url_grades = 'https://synergia.librus.pl/przegladaj_oceny/uczen'
		self.url_events = 'https://synergia.librus.pl/terminarz'
		self.url_login = 'https://synergia.librus.pl/loguj'

		useragent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36'
		useragent += '(KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'
		self.headers = {
			'User-Agent': useragent,
			'Content-Type': 'application/x-www-form-urlencoded',
			'Referer': 'https://synergia.librus.pl/loguj',
			'Accept-Encoding': 'gzip, deflate',
			'Connection': 'keep-alive'
		}
		self.payload = {
			'login': '',
			'passwd': '',
			'ed_pass_keydown': '',
			'ed_pass_keyup': '',
			'captcha': '',
			'jest_captcha': '1',
			'czy_js': '2'
		}

		self.cookies = {
			'_ga': 'GA1.2.2085668300.1439744410',
			'TestCookie': '1'
		}

	def fetch_grades(self, login, password):
		"""fetch_grades(login, password) - fetches grades and returns the HTML.

		Parameters:
		login (string) - login for librus
		password (string) - password for librus
		"""
		self.payload['login'] = login
		self.payload['passwd'] = password
		with requests.Session() as session:
			response = session.post(
				self.url_login,
				data=self.payload, headers=self.headers,
				cookies=self.cookies
			)
			time.sleep(2)
			response = session.get(self.url_grades, headers=self.headers)
		return response.text

	def fetch_events(self, login, password, month, year):
		"""fetch_events(login, password, month, year)
			fetches events and returns the HTML.

		Parameters:
		login (string) - login for librus
		password (string) - password for librus
		month (string) - specified month, 1-12 without prequeling zero
			for ex. 1 instead of 01
		year (string) - specified year in a YYYY format
		"""
		self.payload['login'] = login
		self.payload['passwd'] = password
		with requests.Session() as session:
			response = session.post(
				self.url_login,
				data=self.payload,
				headers=self.headers,
				cookies=self.cookies
			)

			time.sleep(2)

			mini_headers = self.headers
			mini_headers['Referer'] = 'https://synergia.librus.pl/terminarz'
			mini_headers['Origin'] = 'https://synergia.librus.pl'
			mini_payload = {'miesiac': month, 'rok': year}

			response = session.post(
				self.url_events,
				headers=mini_headers,
				data=mini_payload,
				params=mini_payload
			)
			return(response.text)


class Librus:
	"""Librus - allows for control of everything.

	Variables:
	file_handler (FileHandler) - the internal FileHandler
	parser (Parser) - the internal Parser
	grade_book (GradeBook) - the internal GradeBook
	event_calendar (EventCalendar) - the internal EventCalendar
	librus_fetcher (LibrusFetcher) - the internal LibrusFetcher
	login (string) - login to Librus
	password (string) - password to Librus

	Functions:
	update_event_calendar() - Updates the internal event_calendar
	update_grade_book() - Updates the internal grade_book
	"""
	def __init__(self):
		self.file_handler = FileHandler()
		self.parser = Parser()
		self.grade_book = GradeBook()
		self.event_calendar = EventCalendar()
		self.librus_fetcher = LibrusFetcher()
		self.login = ""
		self.password = ""

		self.file_handler.librus = self
		self.parser.librus = self
		self.grade_book.librus = self
		self.event_calendar.librus = self
		self.librus_fetcher.librus = self

	def update_event_calendar(self):
		"""update_event_calendar() - Updates the internal event_calendar.
		Requires user input.
		"""
		print("Choose the method that will be used for getting events data:")
		print("a - Reading from cached data")
		print("b - Getting data straight from Librus")
		while True:
			choice = input("Pick: ").lower()
			if choice in ('a', 'b'):
				break
			else:
				print("Invalid answer - "+choice)
		print("---")

		if choice == 'a':
			print("Picked reading from cached data.")
			month = input("Input desired month (1-12, without the prequeling zero):")
			year = input("Input desired year (YYYY):")
			filename = "events"+month+"_"+year+".pickle"
			temp_event_calendar = self.file_handler.file_to_class(filename)
			self.event_calendar = EventCalendar()
			for event in temp_event_calendar.events:
				self.event_calendar.add(event)  # future proof my code
			self.event_calendar.librus = self
			self.event_calendar.update_old_events(month, year)
			print("Done.")

		elif choice == 'b':
			print("Picked getting data straight from Librus. Updating...")
			if self.login and self.password:
				pass
			else:
				self.login = input("Input your username:")
				self.password = input("Input your password:")

			month = input("Input desired month (1-12, without the prequeling zero):")
			year = input("Input desired year (YYYY):")
			html = self.librus_fetcher.fetch_events(
				self.login, self.password, month, year
			)
			temp_parse = self.parser.parse_html_table(html)
			temp_parse = self.parser.parse_events(temp_parse, html)
			for ev in temp_parse:
				self.event_calendar.add(Event(ev))
			filename = "events"+month+"_"+year+".pickle"
			self.event_calendar.librus = self
			self.event_calendar.update_old_events(month, year)
			self.file_handler.class_to_file(self.event_calendar, filename)
			print("Done.")

	def update_grade_book(self):
		"""update_grade_book() - Updates the internal grade_book.
		Requires user input.
		"""
		print("Choose the method that will be used for getting grades data:")
		print("a - Reading from cached data")
		print("b - Getting data straight from Librus")
		while True:
			choice = input("Pick: ").lower()
			if choice in ('a', 'b'):
				break
			else:
				print("Invalid answer - "+choice)

		print("---")
		if choice == 'a':
			print("Picked reading from cached data.")
			temp_grade_book = self.file_handler.file_to_class("grades.pickle")
			self.grade_book = GradeBook()
			for grade in temp_grade_book.grades:
				self.grade_book.add(grade)  # future proof my code
			self.grade_book.librus = self
			self.grade_book.update_old_grades()
			print("Done.")

		elif choice == 'b':
			print("Picked getting data straight from Librus. Updating...")
			self.login = input("Input your username:")
			self.password = input("Input your password:")
			html = self.librus_fetcher.fetch_grades(self.login, self.password)
			oceny = self.parser.parse_html_grade(html)

			for i in range(len(oceny)):
				if i - 1:   # first grade is a test grade that doesnt parse, so -1
					self.grade_book.add(Grade(self.parser.parse_grade(oceny[i-1])))
			self.file_handler.class_to_file(self.grade_book, "grades.pickle")
			self.grade_book.librus = self
			self.grade_book.update_old_grades()
			print("Done.")


objLibrus = Librus()
objLibrus.update_event_calendar()
objLibrus.update_grade_book()

old_events = objLibrus.event_calendar.compare_old_events()
old_grades = objLibrus.grade_book.compare_old_grades()

old_events.sort_by_day()
old_grades.sort_by_date()

print(old_grades.display())
print(old_events.display())
