from wsgiref.simple_server import make_server

from dranik_framework.main import Framework
from urls import routes, fronts


application = Framework(routes, fronts)

if __name__ == '__main__':
    with make_server('', 8080, application) as httpd:
        print("Запуск на порту 8080...")
        httpd.serve_forever()
