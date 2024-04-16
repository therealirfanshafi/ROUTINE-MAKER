from django.contrib import admin
from .models import *

# Register your models here
admin.site.register(Subject)
admin.site.register(Level)
admin.site.register(Component)
admin.site.register(Option)
admin.site.register(Option_Component)
admin.site.register(Exam)