from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponse
from django.urls import reverse
from json import loads as parse_json
from .models import *


# Create your views here.
class Home(View):
    def get(self, request):
        ctx = dict()
        if request.GET:
            for key in request.GET:
                subjects = Option.objects.filter(level__title=key).order_by('subject__name', 'extension')
                ctx['subjects'] = subjects
        qualifications = Level.objects.all()
        ctx['qualifications'] = qualifications
        return render(request, 'index.html', ctx)


class Routine(View):
    def get(self, request):
        data = parse_json(request.GET['subjects'])
        return HttpResponse(str(data))