from dranik_framework.templator import render


class Index:
    def __call__(self, request):
        return '200 OK', render('index.html', date=request.get('date', None),
                                link=request.get('link', None))


class About:
    def __call__(self, request):
        return '200 OK', render('about.html', date=request.get('date', None),
                                link=request.get('link', None))
