from datetime import date
from views import Index, About, Contact, CreateCategory, CreateCourse, \
    CoursesList, CopyCourse


# front controller
def secret_front(request):
    request['date'] = date.today()


def other_front(request):
    request['link'] = 'https://ya.ru'


fronts = [secret_front, other_front]

# routes = {
#     '/': Index(),
#     '/about/': About(),
#     '/contact/': Contact(),
#     '/create_category/': CreateCategory(),
#     '/create-course/': CreateCourse(),
#     '/courses-list/': CoursesList(),
#     '/copy-course/': CopyCourse(),
# }
