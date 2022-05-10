from copy import deepcopy
from sqlite3 import connect

from patterns.architectural_system_pattern_unit_of_work import DomainObject
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
    def __init__(self, name):
        self.name = name


class Student(User, DomainObject):
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

    def get_student(self, user_name) -> Student:
        for student in self.students:
            if student.name == user_name:
                return student


class StudentMapper:

    def __init__(self, connection):
        self.connection = connection
        self.cursor = connection.cursor()
        self.tablename = 'student'

    def all(self):
        statement = f'SELECT * from {self.tablename}'
        self.cursor.execute(statement)
        result = []
        for item in self.cursor.fetchall():
            id, name = item
            student = Student(name)
            result.append(student)
        return result

    def find_by_id(self, id):
        statement = f"SELECT id, name FROM {self.tablename} WHERE id=?"
        self.cursor.execute(statement, (id,))
        result = self.cursor.fetchone()
        if result:
            return Student(*result)
        else:
            raise RecordNotFoundException(f'record with id={id} not found')

    def insert(self, obj):
        statement = f"INSERT INTO {self.tablename} (name) VALUES (?)"
        self.cursor.execute(statement, (obj.name,))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbCommitException(e.args)

    def update(self, obj):
        statement = f"UPDATE {self.tablename} SET name=? WHERE id=?"

        self.cursor.execute(statement, (obj.name, obj.id))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbUpdateException(e.args)

    def delete(self, obj):
        statement = f"DELETE FROM {self.tablename} WHERE id=?"
        self.cursor.execute(statement, (obj.id,))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbDeleteException(e.args)


connection = connect('patterns.sqlite')


# архитектурный системный паттерн - Data Mapper
class MapperRegistry:
    mappers = {
        'student': StudentMapper,
    }

    @staticmethod
    def get_mapper(obj):

        if isinstance(obj, Student):

            return StudentMapper(connection)

    @staticmethod
    def get_current_mapper(name):
        return MapperRegistry.mappers[name](connection)


class DbCommitException(Exception):
    def __init__(self, message):
        super().__init__(f'Db commit error: {message}')


class DbUpdateException(Exception):
    def __init__(self, message):
        super().__init__(f'Db update error: {message}')


class DbDeleteException(Exception):
    def __init__(self, message):
        super().__init__(f'Db delete error: {message}')


class RecordNotFoundException(Exception):
    def __init__(self, message):
        super().__init__(f'Record not found: {message}')
