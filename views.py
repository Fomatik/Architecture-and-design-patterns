from dranik_framework.templator import render
from patterns.creative_patterns import Engine, Logger

site = Engine()
logger = Logger('main')


class Index:
    def __call__(self, request):
        logger.log('Index page')
        return '200 OK', render('index.html', date=request.get('date', None),
                                link=request.get('link', None),
                                objects_list=site.categories)


class About:
    def __call__(self, request):
        logger.log('About page')
        return '200 OK', render('about.html',
                                date=request.get('date', None),
                                link=request.get('link', None))


class Contact:
    logger.log('Contact page')
    def __call__(self, request):
        return '200 OK', render('contact.html',
                                date=request.get('date', None),
                                link=request.get('link', None))


class CreateCategory:
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


class CreateCourse:
    category_id = -1

    def __call__(self, request):
        logger.log('Create course page')
        if request['method'] == 'POST':
            # метод пост
            data = request['data']

            name = data['name']

            category = site.categories[self.category_id]
            # if self.category_id != -1:
            #     category = site.category_by_id(int(self.category_id))

            course = site.create_course('online', name, category)
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


class CoursesList:
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


class CopyCourse:
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
