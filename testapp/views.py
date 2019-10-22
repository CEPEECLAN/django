from django.http import HttpResponse


def index(request):
    return HttpResponse('Hello, world. Youre at the testapp index. <br> <img src="/static/cepee_logo.png">')
