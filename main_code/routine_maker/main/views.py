from django.shortcuts import render
from django.views import View
from django.http import HttpResponse
from .models import *


# Create your views here.
class Home(View):
    def get(self, request):
        print(request.GET)
        qualifications = Level.objects.all()
        ctx = {'qualifications': qualifications}
        return render(request, 'index.html', ctx)