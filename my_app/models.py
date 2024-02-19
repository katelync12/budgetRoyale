from django.db import models
from django.contrib.auth.models import User
from django import forms


class Student(models.Model):
    grade = models.CharField(max_length=255)
    gpa = models.FloatField()

class User(models.Model):
    email = models.EmailField()
    username = models.CharField(max_length=255, primary_key=True)
    password = models.CharField(max_length=255)
    name = models.CharField(max_length=255)

class Group(models.Model):
    groupID = models.AutoField(primary_key=True)
    groupgoal_id = models.CharField(max_length=255)

class UserJoinGroup(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)

class Category(models.Model):
    category_id = models.CharField(max_length=255, primary_key=True)

class Transactions(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    week = models.DateField()
    amount = models.FloatField()
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

class UserJoinCategory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
