from django.shortcuts import render
from django.views import View
from django.http import FileResponse, HttpResponse
from json import loads as parse_json


import io
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import BaseDocTemplate, PageTemplate, KeepTogether, Frame, PageTemplate, Table
from reportlab.lib.units import cm

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

        exams = Exam.objects.filter(component__in=components).order_by('date', 'session')
        exam_tabulated = [['Date', 'Session', 'Code', 'Subject Name', 'Duration', 'Marks']]
        
        for exam in exams:
            if exam.component.title == "Environment and Development of Bangladesh":
                exam_tabulated.append([exam.date.strftime('%A\n%d %B, %Y\n (%d/%m/%Y)'), exam.session, exam.component, f"{exam.component.subject.name} Paper {exam.component.code[-1]}:\n Environment and\nDevelopment of Bangladesh", exam.component.duration, exam.component.marks ])
            elif exam.component.code[0] == '0':
                exam_tabulated.append([exam.date.strftime('%A\n%d %B, %Y\n (%d/%m/%Y)'), exam.session, exam.component, f"{exam.component.subject.name} Paper {exam.component.code[-1]}:\n{exam.component.title}", exam.component.duration, exam.component.marks ])
            elif exam.component.title == "Fundamental Problem-solving and Programming Skills":
                exam_tabulated.append([exam.date.strftime('%A\n%d %B, %Y\n (%d/%m/%Y)'), exam.session, exam.component, f"{exam.component.subject.name} Paper {exam.component.code[-1]}:\n Fundamental Problem-solving\nand Programming Skills", exam.component.duration, exam.component.marks ])
            else:
                exam_tabulated.append([exam.date.strftime('%A\n%d %B, %Y\n (%d/%m/%Y)'), exam.session, exam.component, f"{exam.component.subject.name} Paper {exam.component.code[0]}:\n{exam.component.title}", exam.component.duration, exam.component.marks ])
    

        buffer = io.BytesIO()

        # adapted from https://stackoverflow.com/questions/63441401/python-reportlab-dynamically-create-new-page-after-first-page-is-completely-fill
        text_frame = Frame(
            x1=0 * cm,  # From left
            y1=0 * cm,  # From bottom
            height=A4[1],
            width=A4[0],
            leftPadding=2 * cm,
            bottomPadding=2 * cm,
            rightPadding=2 * cm,
            topPadding=2 * cm,
            id='text_frame')

        # Building the story
        t = Table(exam_tabulated, splitByRow=True, repeatRows=1)
        t.setStyle([("VALIGN", (0,0), (-1,-1), "MIDDLE"),
                ("ALIGN", (0,0), (-1,-1), "CENTER"),
                ('GRID', (0,0), (-1,-1), 0.25, colors.black),
                ('FONTSIZE',(0,0), (-1,-1), 12)])

        story = [t]
        story.append(KeepTogether([]))

        # Establish a document
        doc = BaseDocTemplate(buffer, pagesize=A4)

        # Creating a page template
        frontpage = PageTemplate(id='FrontPage',
                                frames=[text_frame]
                                )
        # Adding the story to the template and template to the document
        doc.addPageTemplates(frontpage)

        # Building doc
        doc.build(story)

        buffer.seek(0)
        return FileResponse(buffer, filename="Routine.pdf")