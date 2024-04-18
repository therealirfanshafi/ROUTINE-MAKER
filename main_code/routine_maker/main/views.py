# django functionality import
from django.shortcuts import render
from django.views import View
from django.http import FileResponse, HttpResponse
from json import loads as parse_json

# pdf creating import
import io
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import BaseDocTemplate, PageTemplate, KeepTogether, Frame, PageTemplate, Table
from reportlab.lib.units import cm

# import of models
from .models import *


# Create your views here.
class Home(View):

    def get(self, request):

        ctx = dict()
        if request.GET:  # checks if there a qualification level was selected
            for key in request.GET:
                subjects = Option.objects.filter(level__title=key).order_by('subject__name', 'extension')
                ctx['subjects'] = subjects  # retrieves the subjects of the qualification pressed

        qualifications = Level.objects.all()  # retrieves the qualifications
        ctx['qualifications'] = qualifications

        return render(request, 'index.html', ctx)


class Routine(View):

    def get(self, request):

        subjects = parse_json(request.GET['subjects'])  # parses the JSON data in the get request key-value pairs 
        components = list()

        for subject in subjects[:-1]:  # loops over the subjects received (except for the qualification ditc)
            if '(' in subject:  # checks whether the subject has an extension
                # seperates the subject name and extension
                subject = subject.split('(')  
                subject[0] = subject[0][0:-1]
                subject[1] = subject[1][0:-1]

                intermediate_components_list = [x.component for x in Option_Component.objects.filter(option__subject__name=subject[0], option__extension=subject[1], option__level__title=subjects[-1]['qualification'])]  # extracts the components of each subject in an intermediate list, the qualification is retrieved from the last array element and used to filter so that subjects of the same name in different qualifications can be distinguised 

                for component in intermediate_components_list:  # stores the intermediates into the main list
                    components.append(component.id)
                
                
            else:  # same thing for subject without an extension
                intermediate_components_list = [x.component for x in Option_Component.objects.filter(option__subject__name=subject, option__level__title=subjects[-1]['qualification'])]

                for component in intermediate_components_list:
                    components.append(component.id)

        exams = Exam.objects.filter(component__in=components).order_by('date', 'session')  # retrieves the exam dates for the components

        exam_tabulated = [['Date', 'Session', 'Code', 'Subject Name', 'Duration', 'Marks']]  # headings for the pdf table
        
        for exam in exams:  # loops over each exam to format them according to the pdf table format
            if exam.component.title == "Environment and Development of Bangladesh":  # an edge case, the component title is too large to fit into a single line so it is split into 2 lines manually

                exam_tabulated.append([exam.date.strftime('%A\n%d %B, %Y\n (%d/%m/%Y)'), exam.session, exam.component, f"{exam.component.subject.name} Paper {exam.component.code[-1]}:\n Environment and\nDevelopment of Bangladesh", exam.component.duration, exam.component.marks ])

            elif exam.component.code[0] == '0':  # case where the componenent starts with 0; this is done so that the paper number is correct (it is the 2nd digit for these cases)
                exam_tabulated.append([exam.date.strftime('%A\n%d %B, %Y\n (%d/%m/%Y)'), exam.session, exam.component, f"{exam.component.subject.name} Paper {exam.component.code[-1]}:\n{exam.component.title}", exam.component.duration, exam.component.marks ])  # adds formated table data the array

            elif exam.component.title == "Fundamental Problem-solving and Programming Skills":  # similar edge case
                exam_tabulated.append([exam.date.strftime('%A\n%d %B, %Y\n (%d/%m/%Y)'), exam.session, exam.component, f"{exam.component.subject.name} Paper {exam.component.code[-1]}:\n Fundamental Problem-solving\nand Programming Skills", exam.component.duration, exam.component.marks ])

            else:  # case where the compnent does not begin with 0 i.e. here the 1st digit is the paper number
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