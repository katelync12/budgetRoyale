from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from django.db import connection
from django.db import models
from django.http import FileResponse, JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Transactions
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User

# def logout_view(request):
#     logout(request)
#     return redirect('registration/login.html')
@login_required
def send_form(request):
    return redirect('')
@login_required
def create_transaction_page(request):
    current_user = request.user
    categories = UserJoinCategory.objects.filter(user=current_user)

    return render(request, "create_transaction.html", {'categories': categories})

@login_required
def create_personal_goal_page(request):
    current_user = request.user
    categories = UserJoinCategory.objects.filter(user=current_user)

    return render(request, "create_personal_goals.html", {'categories': categories})

@login_required  # Requires the user to be logged in to access this view
def create_personal_goals(request):
    print("create_personal_goals ")
    if request.method == "POST":
        print("create_personal_goals POST")
        amount = float(request.POST.get("amount"))
        category_name = request.POST.get("type")
        is_spending = request.POST.get("goal_type") == "on"
        goal_name = request.POST.get("name")
        goal_start_date = request.POST.get("start_date")
        goal_end_date = request.POST.get("end_date")
        # Access the user who sent the request
        username = request.user.username
        user = User.objects.get(username=username)
        category = None
        if category_name == "":
            category = None
        else:
            try:
                category = Category.objects.get(category_id=category_name)
            except Category.DoesNotExist:
                # Create a new category
                category = Category(category_id=category_name)
                category.save()
        # Check if there's an existing relationship between user and category
        if category:
            try:
                UserJoinCategory.objects.get(user=user, category=category)
            except UserJoinCategory.DoesNotExist:
                # Create a new relationship between user and category
                user_category = UserJoinCategory(user=user, category=category)
                user_category.save()
        
        # If it's a spending, make the amount negative

        # Print out the amount, category, spending/savings status, and the user
        print("Amount:", amount)
        print("Category:", category_name)
        print("Spending:", is_spending)
        print("User:", username)
        personal_goal = PersonalGoal(
            user=user,
            goal_amount=amount,
            goal_name=goal_name,  # Provide a name for the transaction as needed
            category=category,  # Assuming category is a valid value
            sum_transaction = 0,
            is_spending = is_spending,
            start_date = goal_start_date,
            end_date = goal_end_date
        )
        personal_goal.save()
    return redirect('view_personal_goals')

@login_required  # Requires the user to be logged in to access this view
def create_transaction(request):
    if request.method == "POST":
        amount = float(request.POST.get("amount"))
        category_name = request.POST.get("type")
        is_spending = request.POST.get("transaction_type") == "on"
        transaction_name = request.POST.get("name")
        transaction_date = request.POST.get("date")
        
        # Access the user who sent the request
        username = request.user.username
        user = User.objects.get(username=username)
        category = None
        try:
            category = Category.objects.get(category_id=category_name)
        except Category.DoesNotExist:
            # Create a new category
            category = Category(category_id=category_name)
            category.save()

        # Check if there's an existing relationship between user and category
        if category:
            try:
                UserJoinCategory.objects.get(user=user, category=category)
            except UserJoinCategory.DoesNotExist:
                # Create a new relationship between user and category
                user_category = UserJoinCategory(user=user, category=category)
                user_category.save()
        
        # If it's a spending, make the amount negative
        if is_spending:
            amount *= -1

        # Print out the amount, category, spending/savings status, and the user
        print("Amount:", amount)
        print("Category:", category_name)
        print("Spending:", is_spending)
        print("User:", username)
        transaction = Transactions(
            user=user,
            week=transaction_date,  # Assuming you want to record the current date and time
            amount=amount,
            name=transaction_name,  # Provide a name for the transaction as needed
            category=category  # Assuming category is a valid value
        )
        transaction.save()
    return redirect('view_transactions')

@login_required 
def verify_unique_category(request):
    category_name = request.GET.get('name', '')
    username = request.user.username
    user = User.objects.get(username=username)
    category = None
    try:
        category = Category.objects.get(category_id=category_name)
    except Category.DoesNotExist:
        return JsonResponse({'unique': True})
    try:
        UserJoinCategory.objects.get(user=user, category=category)
        return JsonResponse({'unique': False})
    except UserJoinCategory.DoesNotExist:
        return JsonResponse({'unique': True})
    
@login_required 
def add_category(request):
    category_name = request.GET.get('name', '')
    username = request.user.username
    user = User.objects.get(username=username)
    category = None
    if category_name == "":
        category = None
    else:
        try:
            category = Category.objects.get(category_id=category_name)
        except Category.DoesNotExist:
            # Create a new category
            category = Category(category_id=category_name)
            category.save()

    # Check if there's an existing relationship between user and category
    if category:
        try:
            UserJoinCategory.objects.get(user=user, category=category)
        except UserJoinCategory.DoesNotExist:
            # Create a new relationship between user and category
            user_category = UserJoinCategory(user=user, category=category)
            user_category.save()
    return JsonResponse({'category_id': category.category_id})

def add(request):
    # Check if Student table exists
    if not PersonalGoal._meta.db_table in connection.introspection.table_names():
        # Create the Student table if it doesn't exist
        with connection.schema_editor() as schema_editor:
            schema_editor.create_model(PersonalGoal)
            schema_editor.create_model(GroupGoal)

    # Insert a new student named "Mark" with a GPA of 4.0
    mark = Student(grade="Mark", gpa=4.0)
    mark.save()
    all_students = Student.objects.all()

    # Print student data (for demonstration purposes)
    for student in all_students:
        print(f"Student: {student.grade}, GPA: {student.gpa}")

    result = 1
    return JsonResponse({'result': result})

@login_required
def view_transactions(request):
    # Ensure user is authenticated before accessing request.user
    if request.user.is_authenticated:
        current_user = request.user
        
        # Gets all transactions
        username = request.user.username
        user = User.objects.get(username=username)
        transactions = Transactions.objects.all()
        sorted = []
        for transaction in transactions:
            # Only gets the transactions of the currently logged in user
            if (transaction.user.username == username):
                sorted.append(transaction)

        context = {
            'transactions': sorted,
            'current_user': current_user,
        }
        # Render the template with the transactions data
        return render(request, 'view_transactions.html', context)
    else:
        # Redirect to login page if user is not authenticated
        return redirect('login')
    
# Creates an error if the login info is wrong
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # User credentials are correct, log in the user
            login(request, user)
            return redirect('home')  # Redirect to dashboard or any other page
        else:
            # User credentials are incorrect, display an error message
            messages.error(request, "Invalid username or password.")
            return redirect('login')  # Redirect back to the login page
    return render(request, 'registration/login.html')

def delete_transaction(request, transaction_id):
    if request.method == 'POST':
        transaction = Transactions.objects.get(pk=transaction_id)
        transaction.delete()
        return JsonResponse({'message': 'Transaction deleted successfully.'})
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=400)

@login_required 
def group_goals(request):
    # Ensure user is authenticated before accessing request.user
    if request.user.is_authenticated:
        current_user = request.user
        
        if 5 == 5:
            return render(request, 'group_goals.html')
        else:
            return render(request, 'groups.html')
    else:
        # Redirect to login page if user is not authenticated
        return redirect('login')

@login_required
def group_settings(request):
    # Ensure user is authenticated before accessing request.user
    if request.user.is_authenticated:
        current_user = request.user
        
        if 4 == 5:
            return render(request, 'group_settings.html')
        else:
            return render(request, 'groups.html')
    else:
        # Redirect to login page if user is not authenticated
        return redirect('login')
    
@login_required
def leaderboard(request):
    # Ensure user is authenticated before accessing request.user
    if request.user.is_authenticated:
        current_user = request.user
        
        if 4 == 5:
            return render(request, 'leaderboard.html')
        else:
            return render(request, 'groups.html')
    else:
        # Redirect to login page if user is not authenticated
        return redirect('login')