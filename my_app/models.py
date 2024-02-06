from django.db import models
from django.contrib.auth.models import User
from django import forms


class Student(models.Model):
    grade = models.CharField(max_length=255)
    gpa = models.FloatField()

