from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from django.db import connection
from django.db import models
from django.http import FileResponse, JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

# def form(request):
#     return render(request, "form.html")

# def transactions(request):
#     return render(request, "transactions.html")

# def home(request):
#     return render(request, "home.html")


def add(request):
    # Check if Student table exists
    if not Student._meta.db_table in connection.introspection.table_names():
        # Create the Student table if it doesn't exist
        with connection.schema_editor() as schema_editor:
            schema_editor.create_model(Student)
            schema_editor.create_model(User)
            schema_editor.create_model(Group)
            schema_editor.create_model(UserJoinGroup)
            schema_editor.create_model(Category)
            schema_editor.create_model(Transactions)
            schema_editor.create_model(UserJoinCategory)
            print("poppy head")

    # Insert a new student named "Mark" with a GPA of 4.0
    mark = Student(grade="Mark", gpa=4.0)
    mark.save()
    all_students = Student.objects.all()

    # Print student data (for demonstration purposes)
    for student in all_students:
        print(f"Student: {student.grade}, GPA: {student.gpa}")

    result = 1
    return JsonResponse({'result': result})