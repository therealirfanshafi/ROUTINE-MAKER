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
        subjects = parse_json(request.GET['subjects'])
        components = list()
        print(subjects[-1]['qualification'])
        for subject in subjects[:-1]:
            if '(' in subject:
                subject = subject.split('(')
                subject[0] = subject[0][0:-1]
                subject[1] = subject[1][0:-1]
                intermediate_components_list = [x.component for x in Option_Component.objects.filter(option__subject__name=subject[0], option__extension=subject[1], option__level__title=subjects[-1]['qualification'])]
                for component in intermediate_components_list:
                    components.append(component.id)
                
                
            else:
                intermediate_components_list = [x.component for x in Option_Component.objects.filter(option__subject__name=subject, option__level__title=subjects[-1]['qualification'])]
                for component in intermediate_components_list:
                    components.append(component.id)

        exam = Exam.objects.filter(component__in=components)

        return HttpResponse(exam)