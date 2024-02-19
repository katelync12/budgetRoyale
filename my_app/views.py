from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from django.db import connection
from django.db import models
from django.http import FileResponse, JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required  # Requires the user to be logged in to access this view
def create_transaction(request):
    if request.method == "POST":
        amount = float(request.POST.get("amount"))
        category = request.POST.get("type")
        is_spending = request.POST.get("transaction_type") == "on"
        
        # Access the user who sent the request
        user = request.user
        
        # If it's a spending, make the amount negative
        if is_spending:
            amount *= -1

        # Print out the amount, category, spending/savings status, and the user
        print("Amount:", amount)
        print("Category:", category)
        print("Spending:", is_spending)
        print("User:", user)

    return render(request, "create_transaction.html")

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