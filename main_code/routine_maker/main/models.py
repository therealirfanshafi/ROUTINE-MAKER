from django.db import models
from django.core.validators import MinLengthValidator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

# Create your models here.

class Subject(models.Model):
    name = models.CharField(max_length=25)
    code = models.CharField(max_length=4, validators=[MinLengthValidator(4)])


    def __str__(self):
        return f"{self.name} ({self.code})"


class Level(models.Model):
    title = models.CharField(max_length=8)


    def __str__(self):
        return self.title


class Component(models.Model):
    code = models.CharField(max_length=2, validators=[MinLengthValidator(2)])
    title = models.CharField(max_length=50)
    marks = models.IntegerField()
    duration = models.CharField(max_length=20)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    options = models.ManyToManyField('Option', through='Option_Component')


    def __str__(self):
        return f"{self.subject.code}/{self.code}"


class Option(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    extension = models.CharField(max_length=25, blank=True, null=True)
    level = models.ForeignKey(Level, on_delete=models.CASCADE)
    components = models.ManyToManyField('Component', through='Option_Component')

    
    def __str__(self):
        if self.extension:
            return f"{self.level} {self.subject.name} ({self.extension})"
        return f"{self.level} {self.subject.name}"
        

class Option_Component(models.Model):
    option = models.ForeignKey(Option, on_delete=models.CASCADE)
    component = models.ForeignKey(Component, on_delete= models.CASCADE)


    def clean(self):
        if self.option.subject != self.component.subject:
            raise ValidationError(
                _('The subjects and components must match')
            )
        
        super().clean()


    def __str__(self):
        return f"{self.option} Component: {self.component}"

class Exam(models.Model):
    date = models.DateField()
    session = models.CharField(max_length=2, validators=[MinLengthValidator(2)])
    component = models.ForeignKey(Component, on_delete = models.CASCADE)


    def __str__(self):
        return f"{self.component.subject.name} Component {self.component.code} Exam on {self.date}"
