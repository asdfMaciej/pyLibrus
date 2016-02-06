from bs4 import BeautifulSoup


class GradeBook:
	def __init__(self):
		self.grades = []

	def add(self, grade):
		self.grades.append(grade)

	def display(self):
		display_text = ""
		for grade in self.grades:
			display_text += grade.display()
		print(display_text)
		return display_text

	def sort_by_weight(self, reverse=False):
		self.grades.sort(key=lambda x: int(x[8]), reverse=reverse)

	def sort_by_date(self, reverse=False):
		self.grades.sort(key=lambda x: str(x[5]), reverse=reverse)

	def sort_by_grade(self, reverse=False):
		self.grades.sort(key=lambda x: int(x[13]), reverse=reverse)

class Grade:
	def __init__(self, values):
		self.values = [] # Array - For some displaying purposes.

		self.grade_id = 0 # Int - Id of the grade in Librus
		self.grade_numtype = 0 # Int, 0-3, Type of the grade.
		self.grade_type = "" # String,  Description of the type.
		self.school_subject = "" # String, School subject.
		self.grade_value = "" # String, The grade itself.
		self.absolute_value = 0 # Int, absolute value of the grade [+/- removed and taken in account]
		self.date = "" # String, Date in which the grade was written.
		self.day_of_the_week = "" # String, Day of the week in which the grade was written
		self.category = "" # String, The type/category of the grade, for ex. exam/vocal exam
		self.weight = 0 # Int, Weight of the grade.
		self.teacher = "" # String, Teacher which teaches the subject.
		self.calculate_towards_avg_grade = 0 # Int, If the grade calculates to the average.
		self.added = "" # Teacher who added the grade.
		self.description = "" # Description of the grade. Works on ShapingGrade and on some DescriptiveGrade 

		self.update(values)
		self.set_absolute_values()
		self.values.append(self.absolute_value) # values[13]

	def __getitem__(self, index):
		return self.values[index]

	def update(self, values):
		self.values = values

		self.grade_id = values[0]
		self.grade_numtype = values[1]
		self.grade_type = values[2]
		self.school_subject = values[3]
		self.grade_value = values[4]
		self.date = values[5]
		self.day_of_the_week = values[6]
		self.category = values[7]
		self.weight = values[8]
		self.teacher = values[9]
		self.calculate_towards_avg_grade = values[10]
		self.added = values[11]
		self.description = values[12]
		#self.absolute_value = values[13]

	def display(self):
		display_string = "["
		display_string += self.date + ", " + self.day_of_the_week + "] - <" + self.school_subject + "> ("
		display_string += self.grade_value + ")"
		if self.weight != -1:
			display_string += " - Waga: " + str(self.weight)
		if self.calculate_towards_avg_grade != -1:
			display_string += ". Liczy się: "
			display_string += {0: "Nie", 1: "Tak"}[self.calculate_towards_avg_grade]
		display_string += ". Typ oceny: " + self.category
		display_string += ". Dodał/a " + self.teacher + ", id w Librusie: " + str(self.grade_id) + "."
		if self.description:
			display_string += " Opis: "+self.description
		display_string += "\n"
		return display_string

	def set_absolute_values(self):
		if "-" == self.grade_value:
			self.absolute_value = 0
		elif "+" == self.grade_value:
			self.absolute_value = 0
		elif "T" == self.grade_value:
			self.absolute_value = 0
		elif "np" == self.grade_value:
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
		return self.values


class Parser:
	def __init__(self):
		pass

	def ParseGrade(self, grade):
		school_subject = repr(grade.findParents('tr')[0]).split('/tree_colapsed.png"/>')[1].split('<td>')[1].split('</td>')[0]
		grade_id = repr(grade).split("szczegoly/")[1].split('" title')[0]
		grade_value = str(grade.text)
		category = repr(grade).split("Kategoria: ")[1].split('&lt;')[0]
		date = repr(grade).split("Data: ")[1].split('&lt;')[0].split(' (')[0]
		day_of_the_week = repr(grade).split("Data: ")[1].split('&lt;')[0].split(' (')[1].split(')')[0]
		teacher = repr(grade).split('Nauczyciel: ')[1].split('&lt;')[0]
		added = repr(grade).split('Dodał: ')[1].split('&lt;')[0]

		try:
			calculate_towards_avg_grade = {'tak': True, 'nie': False}[repr(grade).split('średniej: ')[1].split('&lt;')[0]]
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
			grade_numtype = has_weight + has_average
			grade_type = {0: "DescriptiveGrade", 1: "MidtermGrade", 2: "StandardGrade"}[grade_numtype]

		try:
			description = repr(grade).split('Ocena: ')[1].split('&lt;')[0]
		except:
			description = ""

		return [grade_id, grade_numtype, grade_type, school_subject, grade_value, date, day_of_the_week, category,
		weight, teacher, calculate_towards_avg_grade, added, description]


def ReadFile(name):
	tFile = open(name, "r", encoding="utf8")
	tContent = tFile.readlines()
	tFile.close()
	return "/n".join(tContent)

def SaveFile(name, content):
	tFile = open(name, "w", encoding="utf8")
	tFile.write(content)
	tFile.close()
	return True

pars = Parser()
dziennik = GradeBook()
html = ReadFile("main.html")
soup = BeautifulSoup(html, "html.parser")
oceny = soup.findAll("a", {"class": "ocena"})
oceny_txt = ""
for i in range(len(oceny)):
	if i - 1: # first grade is no. 0, and doesnt parse due to librus being dumb and putting a >testgrade in html source
		dziennik.add(Grade(pars.ParseGrade(oceny[i-1])))

dziennik.sort_by_grade()
oceny_txt = dziennik.display()
SaveFile("oceny.txt", oceny_txt)