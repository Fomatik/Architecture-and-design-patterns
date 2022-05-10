from copy import deepcopy


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

    def __init__(self, name):
        self.name = name

    @staticmethod
    def log(text):
        print('log--->', text)


class User:
    ...


class Student(User):
    ...


class Teacher(User):
    ...


class UserFactory:
    types = {
        'student': Student,
        'teacher': Teacher,
    }

    def create(self, type_: User) -> User:
        return self.types[type_]()


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


class Course(CoursePrototype):
    auto_id = 0

    def __init__(self, name, category):
        self.id = self.auto_id
        Course.auto_id += 1
        self.name = name
        self.category = category
        self.category.courses.append(self)


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
        self.student = []
        self.categories = []
        self.courses = []

    @staticmethod
    def create_user(type_):
        return UserFactory().create(type_)

    @staticmethod
    def create_category(name):
        return Category(name)

    def category_by_id(self, category_id):
        for category in self.categories:
            if category.id == category_id:
                return category

    @staticmethod
    def create_course(type_, name, category):
        return CourseFactory().create(type_, name, category)

    def get_course(self, course_id):
        for course in self.courses:
            if course.id == course_id:
                return course
