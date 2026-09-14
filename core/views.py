from django.http import HttpResponse



class HomePageView:
    def __call__(self, request):
        return HttpResponse("Welcome to the Holistic Nepal Project!")