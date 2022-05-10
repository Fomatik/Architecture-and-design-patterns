from quopri import decodestring

from dranik_framework.requests import PostRequests, GetRequests
from patterns.creative_patterns import Logger

logger = Logger('main')


class PageNotFound404:
    def __call__(self, request):
        logger.log(f'{self.__class__.__name__} --> '
                   f'{Framework.path}')
        return '404 WHAT', '404 PAGE Not Found'


class Framework:
    # Не нашёл другого способа доступа к переменной в классе для вывода в лог,
    # может вы подскажете?
    path = None

    """Класс Framework - основа фреймворка"""

    def __init__(self, routes_obj, fronts_obj):

        """Конструктор класса Framework"""

        self.routes_lst = routes_obj
        self.fronts_lst = fronts_obj

    def __call__(self, environ, start_response):

        """Метод __call__ вызывается при вызове объекта класса Framework"""

        Framework.path = environ['PATH_INFO']

        if not Framework.path.endswith('/'):
            Framework.path = f'{Framework.path}/'

        request = {'method': environ['REQUEST_METHOD']}

        if request['method'] == 'POST':
            data = PostRequests().get_wsgi_input_params(environ)
            request['data'] = self.decode_value(data)
            logger.log(f'Нам пришли Рost-данные: {request["data"]}')

        if request['method'] == 'GET':
            request_params = GetRequests().get_request_params(environ)
            request['request_params'] = Framework.decode_value(request_params)
            logger.log(f'Нам пришёл GET-запрос: {request["request_params"]}')

        if Framework.path in self.routes_lst:
            view = self.routes_lst[Framework.path]
        else:
            view = PageNotFound404()

        for front in self.fronts_lst:
            front(request)

        code, body = view(request)
        start_response(code, [('Content-Type', 'text/html')])
        return [body.encode('utf-8')]

    @staticmethod
    def decode_value(data):
        new_data = {}
        for k, v in data.items():
            val = bytes(v.replace('%', '=').replace("+", " "), 'UTF-8')
            val_decode_str = decodestring(val).decode('UTF-8')
            new_data[k] = val_decode_str
        return new_data
