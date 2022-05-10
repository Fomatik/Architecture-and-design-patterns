from datetime import date
from views import Index, About, Contact


# front controller
def secret_front(request):
    request['date'] = date.today()


def other_front(request):
    request['link'] = 'https://ya.ru'


fronts = [secret_front, other_front]

routes = {
    '/': Index(),
    '/about/': About(),
    '/contact/': Contact(),
}