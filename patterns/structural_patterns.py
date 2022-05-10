route = {}


class Route:
    def __init__(self, url):
        self.routes = route
        self.url = url

    def __call__(self, cls):
        self.routes[self.url] = cls()


class Debug:
    def __init__(self, view):
        self.view = view

    def __call__(self, cls):
        def timeit(method):
            def timed(*args, **kwargs):
                import time
                start = time.time()
                result = method(*args, **kwargs)
                end = time.time()
                print(f'debug_timeit -> {self.view} выполнялся '
                      f'{end - start:2.2f} '
                      f'seconds')
                return result
            return timed
        return timeit(cls)
