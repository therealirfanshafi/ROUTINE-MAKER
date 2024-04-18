from django.db import models
from django.core.validators import MinLengthValidator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

# Create your models here.

class Subject(models.Model):
    name = models.CharField(max_length=25)  # e.g. Mathematics
    code = models.CharField(max_length=4, validators=[MinLengthValidator(4)])  # e.g. 9709


    def __str__(self):  # str method for the admin user interface
        return f"{self.name} ({self.code})"


class Level(models.Model):
    title = models.CharField(max_length=8)  #e.g. AS Level


    def __str__(self):
        return self.title


class Component(models.Model):
    code = models.CharField(max_length=2, validators=[MinLengthValidator(2)])  # e.g. 12
    title = models.CharField(max_length=50)  # e.g. Multiple Choice
    marks = models.IntegerField()
    duration = models.CharField(max_length=20)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)  # foreign key linking the component to its subject
    options = models.ManyToManyField('Option', through='Option_Component')  # one component may belong to multiple options e.g 9709/12 belongs to many options


    def __str__(self):
        return f"{self.subject.code}/{self.code}"


class Option(models.Model):  # an exam option for a subject
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)  # the subject the option is for
    extension = models.CharField(max_length=25, blank=True, null=True)  # e.g. with Mechanics
    level = models.ForeignKey(Level, on_delete=models.CASCADE)  # the qualification level of the option e.g AS
    components = models.ManyToManyField('Component', through='Option_Component')  # each option consists of many components e.g AS Level Mathematics (with Mechanics) has components 9709/12 and 9709/42

    
    def __str__(self):
        if self.extension:
            return f"{self.level} {self.subject.name} ({self.extension})"
        return f"{self.level} {self.subject.name}"
        

class Option_Component(models.Model):
    option = models.ForeignKey(Option, on_delete=models.CASCADE)
    component = models.ForeignKey(Component, on_delete= models.CASCADE)


    def clean(self):  # validation to make sure that the option and component are for the same subject
        if self.option.subject != self.component.subject:
            raise ValidationError(
                _('The subjects and components must match')
            )
        
        super().clean()


    def __str__(self):
        return f"{self.option} Component: {self.component}"

class Exam(models.Model):
    date = models.DateField()  # an exam date e.g. 30 April, 2024
    session = models.CharField(max_length=2, validators=[MinLengthValidator(2)])  # AM, PM or EV
    component = models.ForeignKey(Component, on_delete = models.CASCADE)  # the component being examined e.g 9709/12


    def __str__(self):
        return f"{self.component.subject.name} Component {self.component.code} Exam on {self.date}"
