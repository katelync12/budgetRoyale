from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from django.db import connection
from django.db import models
from django.http import FileResponse, JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Transactions    
from .models import Group
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from datetime import date
from datetime import timedelta, datetime
from django.http import HttpResponseRedirect

# def logout_view(request):
#     logout(request)
#     return redirect('registration/login.html')

@login_required
def delete_account(request):
    #username = request.user.username
    confirm_name = request.GET.get('name', '')
    
    user = request.user
    if confirm_name != request.user.username:
        messages.error(request, "The name you entered does not match your username. Please try again.")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    if (Group.objects.filter(admin_user=user).exists()):
        messages.error(request, confirm_name + "Please first transfer ownership of your group or delete the group before deleting your account.")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    user.delete()
    return redirect('home')
    
#
@login_required
def send_form(request):
    if request.method == "POST":
        email = request.POST.get("email")
        firstname = request.POST.get("firstname")
        lastname = request.POST.get("lastname")
        subject = request.POST.get("subject")
        send_mail(
            "Form Submission from " + firstname + " " + lastname, 
            "Feedback:\n\n" + subject + "\n\n" + "From: " + email,
            settings.EMAIL_HOST_USER,
            [settings.EMAIL_HOST_USER],
            fail_silently=False
        )
    return redirect('form_confirm')
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
    if not Group._meta.db_table in connection.introspection.table_names():
        # Create the Student table if it doesn't exist
        with connection.schema_editor() as schema_editor:
            schema_editor.create_model(Group)
            schema_editor.create_model(GroupGoal)
            schema_editor.create_model(Transactions)

    # # Insert a new student named "Mark" with a GPA of 4.0
    # mark = Student(grade="Mark", gpa=4.0)
    # mark.save()
    # all_students = Student.objects.all()

    # Print student data (for demonstration purposes)
    # for student in all_students:
    #     print(f"Student: {student.grade}, GPA: {student.gpa}")

    result = 1
    return JsonResponse({'result': result})

@login_required
def view_transactions(request):
    # Ensure user is authenticated before accessing request.user
    if request.user.is_authenticated:
        current_user = request.user
        
        # Gets all transactions
        sorted = []
        username = request.user.username
        week = False
        week = request.GET.get('week') == 'True'
        if (week):
            today = date.today()
            week_ago = today - timedelta(days=7)
            transactions = Transactions.objects.filter(week__gte=week_ago, week__lte=today)
            print("hit")
        else:
            transactions = Transactions.objects.all()
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
def check_user_group(request, page):
    # Ensure user is authenticated before accessing request.user
    if request.user.is_authenticated:
        username = request.user.username
        user = User.objects.get(username=username)
        # Check if there's an existing relationship between user and category
        if UserJoinGroup.objects.filter(user=user).exists():
            return render(request, page + '.html')
        else:
            return redirect('groups')
    else:
        # Redirect to login page if user is not authenticated
        return redirect('login')
    


@login_required  # Requires the user to be logged in to access this view
def create_group(request):
    group_name = request.POST.get("name")
    print(group_name)
    username = request.user.username
    user = User.objects.get(username=username)
    group = None

    if UserJoinGroup.objects.filter(user=user).exists():
        # any popup?
        print("eete")
        return render(request, 'group_settings.html')
    
    group = Group(name=group_name, admin_user=user)
    group.save()
    # Check if there's an existing relationship between user and category
    print(group.name)
    if group:
        try:
            print("try")
            UserJoinGroup.objects.get(user=user, group=group)
        except UserJoinGroup.DoesNotExist:
            # Create a new relationship between user and category
            user_group = UserJoinGroup(user=user, group=group)
            user_group.save()
            print("exception")
    return render(request, 'group_settings.html')

def view_personal_goals(request):
    # Ensure user is authenticated before accessing request.user
    if request.user.is_authenticated:
        current_user = request.user
        
        # Gets all goals
        username = request.user.username
        goals = PersonalGoal.objects.all()
        sorted = []
        for goal in goals:
            # Only gets the transactions of the currently logged in user
            if (goal.user.username == username):
                sorted.append(goal)
        context = {
            'goals': sorted,
            'current_user': current_user,
        }
        # Render the template with the transactions data
        return render(request, 'view_personal_goals.html', context)
    else:
        # Redirect to login page if user is not authenticated
        return redirect('login')
    
def delete_goal(request, goal_id):
    if request.method == 'POST':
        goal = PersonalGoal.objects.get(pk=goal_id)
        goal.delete()
        return JsonResponse({'message': 'Goal deleted successfully.'})
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=400)

def edit_transaction_action(request, transaction_id):
    transaction = get_object_or_404(Transactions, pk=transaction_id)
    if request.method == 'POST':
        # Retrieve the form data from the POST request
        week = request.POST.get('date')
        amount = request.POST.get('amount')
        name = request.POST.get('name')
        category_id = request.POST.get('type')
        is_spending = request.POST.get("transaction_type") == "on"
        if is_spending:
            amount = str(float(amount) * -1)
        
        # Update the transaction object with the new data
        category = Category.objects.get(category_id=category_id)
        transaction.week = week
        transaction.amount = amount
        transaction.name = name
        transaction.category = category
        transaction.save()
        return redirect('view_transactions')
    
    # Retrieve all categories for populating the dropdown
    categories = Category.objects.all()
    is_negative = transaction.amount < 0
    if is_negative:
        transaction.amount = abs(transaction.amount)
    
    return render(request, 'edit_transaction.html', {'transaction': transaction, 'categories': categories, 'is_negative': is_negative})

def edit_personal_goal_action(request, goal_id):
    goal = get_object_or_404(PersonalGoal, pk=goal_id)
    if request.method == 'POST':
        # Retrieve the form data from the POST request
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        amount = request.POST.get('amount')
        name = request.POST.get('name')
        category_id = request.POST.get('type')
        is_spending = request.POST.get("goal_type") == "on"
    
        if is_spending:
            amount = str(float(amount) * -1)
        category = Category.objects.get(category_id=category_id)
        goal.start_date = start_date
        goal.end_date = end_date
        goal.goal_amount = amount
        goal.goal_name = name
        goal.category= category
        goal.is_spending = is_spending
        goal.save()

        return redirect('view_personal_goals')
    
    # Retrieve all categories for populating the dropdown
    categories = Category.objects.all()
    if goal.is_spending:
        goal.goal_amount = abs(goal.goal_amount)
    
    return render(request, 'edit_personal_goal.html', {'goal': goal, 'categories': categories, 'is_spending': goal.is_spending})

@login_required
def generate_expenses_pie_chart(request):
    start_date_str = request.GET.get('start_date')
    end_date_str = request.GET.get('end_date')

    # Convert date strings to datetime objects
    start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date() if start_date_str else None
    end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date() if end_date_str else None

    # Filter transactions with negative amounts
    negative_transactions = Transactions.objects.filter(amount__lt=0)

    if start_date:
        negative_transactions = negative_transactions.filter(week__gte=start_date)
    if end_date:
        negative_transactions = negative_transactions.filter(week__lte=end_date)

    username = request.user

    # Aggregate expenses based on categories
    category_spending = {}
    for transaction in negative_transactions:
        if (str(transaction.user.username) == str(username)):
            category_name = transaction.category.category_id
            if category_name in category_spending:
                category_spending[category_name] += transaction.amount * -1
            else:
                category_spending[category_name] = transaction.amount * -1

    # Prepare data for the pie chart
    labels = list(category_spending.keys())
    data = list(category_spending.values())

    chart_data = {
        'labels': labels,
        'data': data,
    }
    return JsonResponse(chart_data)

@login_required
def generate_income_pie_chart(request):
    start_date_str = request.GET.get('start_date')
    end_date_str = request.GET.get('end_date')

    # Convert date strings to datetime objects
    start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date() if start_date_str else None
    end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date() if end_date_str else None

    positive_transactions = Transactions.objects.filter(amount__gt=0)

    if start_date:
        positive_transactions = positive_transactions.filter(week__gte=start_date)
    if end_date:
        positive_transactions = positive_transactions.filter(week__lte=end_date)

    username = request.user

    # Aggregate spendings based on categories
    category_income = {}
    for transaction in positive_transactions:
        if (str(transaction.user.username) == str(username)):
            category_name = transaction.category.category_id
            if category_name in category_income:
                category_income[category_name] += transaction.amount
            else:
                category_income[category_name] = transaction.amount

    # Prepare data for the pie chart
    labels = list(category_income.keys())
    data = list(category_income.values())

    chart_data = {
        'labels': labels,
        'data': data,
    }
    print(chart_data)
    return JsonResponse(chart_data)

def leave_group(request):
    
    

    return redirect('groups')