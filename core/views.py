from django.http import HttpResponse
from django.shortcuts import render


class HomePageView:
    def __call__(self, request):
        return render(request, 'core/index.html')