from numpy import mean

all_students = []
all_lectures = []

class Person:
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.grades = {}
        self.average_grades = ''

    def get_all_average_grade(self):
        grades = []
        for v in self.grades.values():
            grades += v
            return mean(grades)

    def get_average_grade_per_course(self):
        average_grade_per_course = {}
        for key, value in self.grades.items():
            average_grade_per_course[key] = value
        return average_grade_per_course

class Student(Person):

    def __init__(self, name, surname, gender):
        super().__init__(name, surname)
        self.gender = gender
        self.finished_courses = []
        self.courses_in_progress = []
        all_students.append(self)

    def __str__(self):
        courses = []
        finished_courses = ''
        for i in self.courses_in_progress:
            courses.append(i)
        for i in self.finished_courses:
            finished_courses += f'{i}'
        for k, v in self.get_average_grade_per_course().items():
            self.average_grades += f'Средняя оценка за домашние задания {k}: {mean(v)}\n'
        return f'\nИмя: {self.name} \nФамилия: {self.surname}\n{self.average_grades}'\
               f'Курсы в процессе изучения: {",".join(courses)}\n'\
               f'Завершенные курсы: {finished_courses}\n'

    def __ge__(self, other):
        return self.get_all_average_grade() >= other.get_all_average_grade()

    def __le__(self, other):
        return self.get_all_average_grade() <= other.get_all_average_grade()

    def rate_mentor (self, lecturer, course, grade):
        if isinstance(lecturer, Lecturer) and course in lecturer.courses_attached and course in self.courses_in_progress:
            if course in lecturer.grades:
                lecturer.grades[course] += [grade]
            else:
                lecturer.grades[course] = [grade]
        else:
            return 'Ошибка'


class Mentor(Person):
    def __init__(self, name, surname):
        super().__init__(name, surname)
        self.courses_attached = []


class Lecturer(Mentor):
    def __init__(self, name, surname):
        super().__init__(name, surname)
        all_lectures.append(self)

    def __str__(self):
        for k, v in self.get_average_grade_per_course().items():
            self.average_grades += f'Средняя оценка за лекции {k}: {mean(v)}\n'
        return f'\nИмя: {self.name}\nФамилия: {self.surname}\n{self.average_grades}'

    def __ge__(self, other):
        return self.get_all_average_grade() >= other.get_all_average_grade()

    def __le__(self, other):
        return self.get_all_average_grade() <= other.get_all_average_grade()


class Reviewer(Mentor):
    def __init__(self, name, surname):
        super().__init__( name, surname)

    def rate_hw(self, student, course, grade):
        if isinstance(student, Student) and course in self.courses_attached and course in student.courses_in_progress:
            if course in student.grades:
                student.grades[course] += [grade]
            else:
                student.grades[course] = [grade]
        else:
            return 'Ошибка'

    def __str__(self):
        return f'Имя: {self.name} \nФамилия: {self.surname}'

    def get_all_studs_grades(students=all_students, course='Python'):
        res = []
        for student in students:
            if course in student.grades.keys():
                for i in student.grades.values():
                    res += i
                    return f'Средняя отметка всех студентов по предмету {course}: {mean(res)}'

    def get_all_lectures_grades(lectures=all_lectures, course='Python'):
        res = []
        for lectures in Lecturer:
            if course in lectures.grades.keys():
                for i in lectures.grades.values():
                    res += i
                    return f'Средняя отметка всех преподавателей по предмету {course}: {mean(res)}'
                else:
                    return 'Оценок еще нет'


best_student = Student('Ruoy', 'Eman', 'your_gender')
best_student.courses_in_progress += ['Python']
best_student.courses_in_progress += ['GIT']
best_student.finished_courses = ['Введение в программирование']

not_best_student = Student('Vladimir', 'Vavilov', 'male')
not_best_student.courses_in_progress += ['Python']
not_best_student.courses_in_progress += ['GIT']
not_best_student.finished_courses = ['Нет таких курсов у Володи']

cool_reviewer = Reviewer('Some', 'Buddy')
cool_reviewer.courses_attached = ['Python']
cool_reviewer.courses_attached = ['GIT']
cool_reviewer.rate_hw(best_student, 'Python', 6)
cool_reviewer.rate_hw(best_student, 'GIT', 4)
cool_reviewer.rate_hw(best_student, 'Python', 10)
cool_reviewer.rate_hw(not_best_student, 'GIT', 8)
cool_reviewer.rate_hw(not_best_student, 'Python', 10)

second_cool_reviewer = Reviewer('Some', 'Buddy')
second_cool_reviewer.courses_attached += ['Python']
second_cool_reviewer.rate_hw(best_student, 'Python', 7)
second_cool_reviewer.rate_hw(best_student, 'GIT', 10)
second_cool_reviewer.rate_hw(not_best_student, 'Python', 3)
second_cool_reviewer.rate_hw(not_best_student, 'GIT', 9)

cool_lecturer = Lecturer('Mikhail', 'Antonov')
cool_lecturer.courses_attached += ['Python']
cool_lecturer.courses_attached += ['GIT']

second_cool_lecturer = Lecturer('Oleg', 'Bylugin')
second_cool_lecturer.courses_attached += ['Python']
second_cool_lecturer.courses_attached += ['GIT']

not_best_student.rate_mentor(cool_lecturer, 'GIT', 3)
not_best_student.rate_mentor(cool_lecturer, 'Python', 4)
not_best_student.rate_mentor(second_cool_lecturer, 'GIT', 5)
not_best_student.rate_mentor(second_cool_lecturer, 'GIT', 8)
not_best_student.rate_mentor(second_cool_lecturer, 'Python', 7)
not_best_student.rate_mentor(second_cool_lecturer, 'Python', 10)

best_student.rate_mentor(cool_lecturer, 'Python', 8)
best_student.rate_mentor(cool_lecturer, 'GIT', 10)
best_student.rate_mentor(cool_lecturer, 'Python', 5)

best_student.rate_mentor(second_cool_lecturer, 'Python', 6)
best_student.rate_mentor(second_cool_lecturer, 'Python', 3)
best_student.rate_mentor(second_cool_lecturer, 'GIT', 10)
best_student.rate_mentor(second_cool_lecturer, 'GIT', 5)
not_best_student.rate_mentor(cool_lecturer, 'GIT', 5)
not_best_student.rate_mentor(cool_lecturer, 'Python', 7)


print(cool_reviewer)
print(second_cool_lecturer)
print(cool_lecturer)
print(best_student)
print(not_best_student)