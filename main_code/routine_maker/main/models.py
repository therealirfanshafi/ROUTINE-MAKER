from django.db import models
from django.core.validators import MinLengthValidator


# Create your models here.

class Subject(models.Model):
    code = models.CharField(max_length=4, validators=[MinLengthValidator(4)])


    def __str__(self):
        return self.code


class Level(models.Model):
    title = models.CharField(max_length=8)


    def __str__(self):
        return self.title


class Component(models.Model):
    code = models.CharField(max_length=2, validators=[MinLengthValidator(2)])
    title = models.CharField(max_length=20)
    marks = models.IntegerField()
    duration = models.CharField(max_length=20)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    options = models.ManyToManyField('Option', through='Option_Component')


    def __str__(self):
        return f"{self.subject.code}/{self.code}"


class Option(models.Model):
    name = models.CharField(max_length=10)
    extension = models.CharField(max_length=15, null=True)
    level = models.ForeignKey(Level, on_delete=models.CASCADE)
    components = models.ManyToManyField('Component', through='Option_Component')

    
    def __str__(self):
        return self.name

class Option_Component(models.Model):
    option = models.ForeignKey(Option, on_delete=models.CASCADE)
    component = models.ForeignKey(Component, on_delete= models.CASCADE)


class Exam(models.Model):
    date = models.DateField()
    session = models.CharField(max_length=2, validators=[MinLengthValidator(2)])
    component = models.ForeignKey(Component, on_delete = models.CASCADE)
