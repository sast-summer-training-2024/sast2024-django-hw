from django.db import models


class Student(models.Model):
    id = models.CharField(max_length=10, primary_key=True)

    name = models.CharField(max_length=50)

    selectedCourses = models.ManyToManyField('Course', related_name='students')


class Course(models.Model):
    id = models.CharField(max_length=10, primary_key=True)

    name = models.CharField(max_length=50)

    teacher = models.CharField(max_length=50)

    department = models.CharField(max_length=50)

    time = models.CharField(max_length=50)
