from django.http import HttpRequest, HttpResponse


# Create your views here.
def login_view(request: HttpRequest):
    return HttpResponse('login')


def logout_view(request: HttpRequest):
    return HttpResponse('logout')
