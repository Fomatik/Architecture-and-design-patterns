from copy import deepcopy

from patterns.behavioral_patterns import Subject, FileWriter, ConsoleWriter


class LoggerSingletonName(type):

    def __init__(cls, name, bases, attrs, **kwargs):
        super().__init__(name, bases, attrs)
        cls.__instance = {}

    def __call__(cls, *args, **kwargs):
        name = None
        if args:
            name = args[0]
        if kwargs:
            name = kwargs['name']

        if name in cls.__instance:
            return cls.__instance[name]
        else:
            cls.__instance[name] = super().__call__(*args, **kwargs)
            return cls.__instance[name]


class Logger(metaclass=LoggerSingletonName):

    def __init__(self, name, writer=FileWriter()):
        self.name = name
        self.writer = writer

    def log(self, text):
        text = f'log---> {text}'
        self.writer.write(text)


class User:
    auto_id = 0

    def __init__(self, name):
        self.name = name
        self.id = self.auto_id
        User.auto_id += 1


class Student(User):
    def __init__(self, name):
        self.courses = []
        super().__init__(name)


class Teacher(User):
    ...


class UserFactory:
    types = {
        'student': Student,
        'teacher': Teacher,
    }

    def create(self, type_: User, name) -> User:
        return self.types[type_](name)


class Category:
    auto_id = 0

    def __init__(self, name):
        self.id = self.auto_id
        Category.auto_id += 1
        self.name = name
        self.courses = []
        Logger('main').log(f'Category \'{self.name}\' created')

    def courses_count(self):
        return len(self.courses)


class CoursePrototype:
    @staticmethod
    def copy(obj):
        new_course = deepcopy(obj)
        new_course.id = Course.auto_id
        Course.auto_id += 1
        Logger('main').log(
            f'Course \'{new_course.name}\' created from \'{obj.name}\'')
        return new_course


class Course(CoursePrototype, Subject):
    auto_id = 0

    def __init__(self, name, category):
        self.id = self.auto_id
        Course.auto_id += 1
        self.name = name
        self.category = category
        self.category.courses.append(self)
        self.students = []
        super().__init__()

    def __getitem__(self, item):
        return self.students[item]

    def add_student(self, student: Student):
        self.students.append(student)
        student.courses.append(self)
        self.notify()


class OfflineCourse(Course):
    ...


class OnlineCourse(Course):
    ...


class CourseFactory:
    types = {
        'offline': OfflineCourse,
        'online': OnlineCourse,
    }

    def create(self, type_, name, category) -> Course:
        Logger('main').log(
            f'CourseFactory.create({type_ = }, {name = }, {category.name = })')
        return self.types[type_](name, category)


class Engine:
    def __init__(self):
        self.teacher = []
        self.students = []
        self.categories = []
        self.courses = []

    @staticmethod
    def create_user(type_, name):
        return UserFactory().create(type_, name)

    @staticmethod
    def create_category(name):
        return Category(name)

    @staticmethod
    def create_course(type_, name, category):
        return CourseFactory().create(type_, name, category)

    def category_by_id(self, category_id):
        for category in self.categories:
            if category.id == category_id:
                return category

    def get_course(self, course_id):
        for course in self.courses:
            if course.id == course_id or course.name == course_id:
                return course

    def get_student(self, user_id) -> Student:
        for student in self.students:
            if student.id == user_id or student.name == user_id:
                return student
