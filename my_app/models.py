from django.db import models
from django.contrib.auth.models import User
from django import forms
from django.db import connection

class Student(models.Model):
    grade = models.CharField(max_length=255)
    gpa = models.FloatField()

class Group(models.Model):
    name = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    admin_user = models.ForeignKey(User, on_delete=models.CASCADE)
    

class UserJoinGroup(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)

class Category(models.Model):
    category_id = models.CharField(max_length=255, primary_key=True)


class UserJoinCategory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

class PersonalGoal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    goal_amount = models.FloatField()
    sum_transaction = models.FloatField(default=0)
    is_spending = models.BooleanField(default=True)
    start_date = models.DateField()
    end_date = models.DateField()
    goal_name = models.CharField(max_length=255)

class GroupGoal(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    amount = models.FloatField()
    sum_transaction = models.FloatField(default=0)
    is_spending = models.BooleanField(default=True)
    start_date = models.DateField()
    end_date = models.DateField()
    goal_name = models.CharField(max_length=255)
    is_primary = models.BooleanField(default=False)
    is_overall = models.BooleanField(default=False)

class Transactions(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    week = models.DateField()
    amount = models.FloatField()
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    group_goal = models.ForeignKey(GroupGoal, on_delete=models.SET_NULL, null=True, blank=True)