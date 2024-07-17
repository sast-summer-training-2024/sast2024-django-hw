from django.contrib.auth.models import User
from django.db import models


class Student(models.Model):
    id = models.CharField(max_length=10, primary_key=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    selectedCourses = models.ManyToManyField('Course', related_name='students', blank=True)


class Course(models.Model):
    id = models.CharField(max_length=10, primary_key=True)

    name = models.CharField(max_length=50)

    teacher = models.CharField(max_length=50)

    department = models.CharField(max_length=50)

    time = models.CharField(max_length=50)
