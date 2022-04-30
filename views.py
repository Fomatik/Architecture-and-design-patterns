from dranik_framework.templator import render
from patterns.behavioral_patterns import ListView, CreateView, FileWriter, \
    ConsoleWriter, EmailNotifier, SmsNotifier, BaseSerializer
from patterns.creative_patterns import Engine, Logger
from patterns.structural_patterns import Route, Debug

site = Engine()
logger = Logger('main', ConsoleWriter())
email_notifier = EmailNotifier()
sms_notifier = SmsNotifier()


@Route('/')
class Index:
    @Debug(view='Index')
    def __call__(self, request):
        logger.log('Index page')
        return '200 OK', render('index.html', date=request.get('date', None),
                                link=request.get('link', None),
                                objects_list=site.categories)


@Route('/about/')
class About:
    @Debug(view='About')
    def __call__(self, request):
        logger.log('About page')
        return '200 OK', render('about.html',
                                date=request.get('date', None),
                                link=request.get('link', None))


@Route('/contact/')
class Contact:
    @Debug(view='Contact')
    def __call__(self, request):
        logger.log('Contact page')
        return '200 OK', render('contact.html',
                                date=request.get('date', None),
                                link=request.get('link', None))


@Route('/create_category/')
class CreateCategory:
    @Debug(view='CreateCategory')
    def __call__(self, request):
        logger.log('Create category page')
        if request['method'] == 'POST':
            data = request['data']
            name = data['name']
            new_category = site.create_category(name)
            site.categories.append(new_category)
            return '200 OK', render('index.html',
                                    date=request.get('date', None),
                                    link=request.get('link', None),
                                    objects_list=site.categories)
        else:
            return '200 OK', render('create_category.html',
                                    date=request.get('date', None),
                                    link=request.get('link', None))


@Route('/create-course/')
class CreateCourse:
    category_id = -1

    @Debug(view='CreateCourse')
    def __call__(self, request):
        logger.log('Create course page')
        if request['method'] == 'POST':
            # метод пост
            data = request['data']

            name = data['name']

            category = site.categories[self.category_id]

            course = site.create_course('online', name, category)

            course.observers.append(email_notifier)
            course.observers.append(sms_notifier)

            site.courses.append(course)

            return '200 OK', render('courses_list.html',
                                    objects_list=category.courses,
                                    name=category.name,
                                    id=category.id)

        else:
            try:
                self.category_id = int(request['request_params']['id'])
                category = site.category_by_id(int(self.category_id))

                return '200 OK', render('create_course.html',
                                        name=category.name,
                                        id=category.id)
            except KeyError:
                return '200 OK', 'No categories have been added yet'


@Route('/courses-list/')
class CoursesList:
    @Debug(view='CoursesList')
    def __call__(self, request):
        logger.log('Courses list page')
        try:
            category = site.category_by_id(
                int(request['request_params']['id']))
            return '200 OK', render('courses_list.html',
                                    objects_list=category.courses,
                                    name=category.name, id=category.id)
        except KeyError:
            return '200 OK', 'No courses have been added yet'


@Route('/copy-course/')
class CopyCourse:
    @Debug(view='CopyCourse')
    def __call__(self, request):
        logger.log('Copy course')
        request_params = request['request_params']

        course_id = int(request_params['id'])
        course = site.get_course(course_id)
        category = site.category_by_id(int(course.category.id))
        if course:
            new_course = course.copy(course)
            if not new_course.name.startswith('copy_'):
                new_course.name = f'copy_{course.name}'
            site.courses.append(new_course)
            category.courses.append(new_course)
            return '200 OK', render('courses_list.html',
                                    objects_list=category.courses,
                                    name=course.category.name,
                                    id=course.category.id)


@Route('/student-list/')
class StudentListView(ListView):
    queryset = site.students
    template_name = 'student_list.html'


@Route('/create-student/')
class StudentCreateView(CreateView):
    template_name = 'create_student.html'

    def create_obj(self, data: dict):
        name = data['name']
        new_obj = site.create_user('student', name)
        site.students.append(new_obj)


@Route('/add-student/')
class AddStudentByCourseCreateView(CreateView):
    template_name = 'add_student.html'

    def get_context_data(self):
        context = super().get_context_data()
        context['courses'] = site.courses
        context['students'] = site.students
        return context

    def create_obj(self, data: dict):
        course_name = data['course_name']
        course = site.get_course(course_name)
        student_name = data['student_name']
        student = site.get_student(student_name)
        course.add_student(student)


@Route('/api/')
class CourseApi:
    @Debug(view='CourseApi')
    def __call__(self, request):
        return '200 OK', BaseSerializer(site.courses).save()
