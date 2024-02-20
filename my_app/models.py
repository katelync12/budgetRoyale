from django.db import models
from django.contrib.auth.models import User
from django import forms
from django.db import connection
import pgtrigger

class Student(models.Model):
    grade = models.CharField(max_length=255)
    gpa = models.FloatField()


class Group(models.Model):
    groupID = models.AutoField(primary_key=True)
    groupgoal_id = models.CharField(max_length=255)

class UserJoinGroup(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)

class Category(models.Model):
    category_id = models.CharField(max_length=255, primary_key=True)

@pgtrigger.register(
    pgtrigger.Trigger(
        name='print_hello_world',
        level=pgtrigger.Row,
        when=pgtrigger.After,
        operation=pgtrigger.Insert,
        func=f'''
            -- Print "Hello, World!" when a new row is inserted into Transactions
            RAISE NOTICE 'Hello, World!';
            RETURN NULL;
        ''',
    )
)
class Transactions(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    week = models.DateField()
    amount = models.FloatField()
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

class UserJoinCategory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

class PersonalGoal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    goal_amount = models.FloatField()
    sum_transaction = models.FloatField(default=0)
    is_spending = models.BooleanField(default=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

class GroupGoal(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    amount = models.FloatField()
    sum_transaction = models.FloatField(default=0)
    is_spending = models.BooleanField(default=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()