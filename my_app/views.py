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
from django.urls import reverse
from datetime import date
from datetime import timedelta, datetime
from django.http import HttpResponseRedirect
from django.db.models import Sum
import json
from django_user_agents.utils import get_user_agent
import colorsys
#HELPER, DO NOT ADD LOGIN REQUIRED
def calculate_weekly_savings(user):
    # Get the start and end date for the past week
    end_date = datetime.now()
    start_date = end_date - timedelta(days=7)
    
    # Query transactions for the user within the past week with positive amounts
    weekly_transactions = Transactions.objects.filter(user=user, 
                                                      amount__gt=0, 
                                                      week__range=(start_date, end_date))  
    # Calculate total savings
    total_savings = sum(transaction.amount for transaction in weekly_transactions)
    
    return total_savings

def calculate_weekly_spendings(user):
    # Get the start and end date for the past week
    end_date = datetime.now()
    start_date = end_date - timedelta(days=7)
    
    # Query transactions for the user within the past week with positive amounts
    weekly_transactions = Transactions.objects.filter(user=user, 
                                                      amount__lt=0, 
                                                      week__range=(start_date, end_date))  
    # Calculate total savings
    total_savings = sum(transaction.amount for transaction in weekly_transactions)
    
    return total_savings * -1

def send_subscription_email(user_id):
    try:
        # Retrieve the user object using the user_id
        user = User.objects.get(id=user_id)
        # Get the email address of the user
        user_email = user.email

        # Determine if the user is associated with any groups
        user_groups = UserJoinGroup.objects.filter(user=user)
        group_message = "You are not currently in any groups. You should consider joining a group to improve your budgeting experience."
        if user_groups.exists():
            # If the user is in at least one group, get the name of the first group
            first_group_name = user_groups.first().group.name
            group_message = f"You are currently in a group named '{first_group_name}'."


        # Send email to the user's email address
        send_mail(
            f"Hello {user.username}",
            f"This is your weekly subscription email. Here are some insights into your spending and savings this week:\n"
            f"You saved: ${calculate_weekly_savings(user)}\n"
            f"You spent: ${calculate_weekly_spendings(user)}\n\n"
            f"{group_message}\n\n"
            "We hope you enjoy your week. Keep budgeting!\n"
            "Best, Budget Royale Team",
            settings.EMAIL_HOST_USER,
            [user_email],  # Sending email to the user's email address
            fail_silently=False
        )
    except User.DoesNotExist:
        # Handle the case where the user does not exist
        # You can log this or perform any other necessary actions
        pass  # Or raise an appropriate exception
def hex_to_rgb(hex_color):
    # Remove '#' symbol if present
    hex_color = hex_color.lstrip('#')
    # Convert hex to RGB
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)
    return r, g, b

@login_required
def spendings_breakdown(request):
    #DEFAULT DATES
    end_date = datetime.now()
    start_date = end_date - timedelta(days=7)
    print("spendings_breakdown")

    user = request.user

    leaderboard = []
    
    # Get all group IDs that the user is a part of
    user_groups = UserJoinGroup.objects.filter(user=user).values_list('group', flat=True)
    if not user_groups:
        return redirect('groups')
    # Get all users in the same groups as the current user
    leaderboard_users = UserJoinGroup.objects.filter(group__in=user_groups).select_related('user')
    print(leaderboard_users)
    # Iterate through each user
    for user_group in leaderboard_users:
        print(str(user_group.user) + "is user")
        print("go wow wow")
        transactions = Transactions.objects.filter(
        user=user_group.user,
        amount__lt=0,
        week__range=(start_date, end_date))

# Calculate total score as the sum of negative amounts
        total_score = 0

# If total_score is None (i.e., no transactions found), set it to 0
        if transactions is not None:
            total_score = transactions.aggregate(total_score=Sum('amount'))['total_score'] * -1

        color = None
        try:
            user_profile = UserProfile.objects.get(user=user_group.user)
            color = user_profile.color  # Get user's color from UserProfile
        except:
            pass
        # Append user's name and total score to the leaderboard
        leaderboard.append({'name': user_group.user.username, 'score': total_score, 'color': color})
    
    # Sort the leaderboard by score in descending order
    leaderboard.sort(key=lambda x: x['score'], reverse=True)
    
    context = {
        'leaderboard': leaderboard,  # Pass the primary group goal's name in the context
    }
    return render(request, 'spendings_breakdown.html', context)

@login_required
def profile_settings(request):
    print("profile_settings")
    user = request.user
    user_profile = UserProfile.objects.filter(user=user).first()
    color = user_profile.color if user_profile and user_profile.color else ''
    
    # Calculate hue value
    hue_value = 0
    val = "0%"
    if color:
        # Parse the color to get RGB components
        r, g, b = hex_to_rgb(color)

        # Convert RGB to HSL
        h, s, l = colorsys.rgb_to_hls(r / 255.0, g / 255.0, b / 255.0)

        # Convert hue to degrees
        hue_value = int(h * 360)
        val = str((hue_value / 360) * 100) + '%'  # Calculate the hue value as a percentage
    context = {
        'color': color,
        'val': val,
        'hue': hue_value,
        'subscribed': SubscriberList.objects.filter(user=user).exists()
    }
    print(color)
    print(hue_value)
    print(val)
    return render(request, 'profile_settings.html', context)
@login_required
def clear_session_filter(request):
    request.session['selected_categories'] = []
    request.session['start_date_str'] = None
    request.session['end_date_str'] = None
    return redirect('view_transactions')
@login_required 
def add_session_filter(request):
    current_user = request.user
    selected_categories = request.GET.getlist('selected_categories')
    start_date_str = request.GET.get('start_date')
    end_date_str = request.GET.get('end_date')
    if start_date_str is not None:
        request.session['start_date_str'] = start_date_str

    # Check if end_date_str exists in the form
    if end_date_str is not None:
        request.session['end_date_str'] = end_date_str

    # Check if selected_categories exists in the form
    if selected_categories:
        request.session['selected_categories'] = selected_categories
    return redirect('view_transactions')
@login_required
def update_profile_color(request):
        # Parse JSON data from request body
        color = request.GET.get('color', '')
        print(str(color) + "color")
        
        user = request.user
        
        # Get or create UserProfile for the user
        user_profile, created = UserProfile.objects.get_or_create(user=user)
        
        # Update color and save the UserProfile object
        user_profile.color = color
        user_profile.save()
        
        # Return success response
        return JsonResponse({'message': 'Profile color updated successfully!'}, status=200)


@login_required
def view_group_goals(request):
    #TODO: implement
    return redirect('home')
@login_required
def delete_group(request, group_id):
    if request.method == 'POST':
        user = request.user
        group = Group.objects.get(pk=group_id)
        if user == group.admin_user:
            group.delete()
            messages.success(request, "Group deleted successfully.")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        else:
            messages.error(request, "You are not the admin of this group.")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    else:
        messages.error(request, "Failed to process delete group request.")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    
@login_required
def group_leaderboard(request):
    user = request.user
    print("group_leaderboard")
    leaderboard = []
    
    # Get all group IDs that the user is a part of
    user_groups = UserJoinGroup.objects.filter(user=user).values_list('group', flat=True)
    if not user_groups:
        return redirect('groups')
    # Get all users in the same groups as the current user
    leaderboard_users = UserJoinGroup.objects.filter(group__in=user_groups).select_related('user')
    
    # Get the name of the primary group goal
    primary_group_goal = GroupGoal.objects.filter(group__in=user_groups, is_primary=True).first()
    if (primary_group_goal == None):
        return redirect('group_settings')
    # Iterate through each user
    for user_group in leaderboard_users:
        # skip if user has opted out
        try:
            profile = UserProfile.objects.get(user=user_group.user)
            if profile != None and not profile.opt_in:
                if request.user == user_group.user:
                    opted = False
                continue
            else:
                opted = True
        except:
            if request.user == user_group.user:
                opted = True

        # Initialize variables to store transaction amounts for savings and spendings
        total_score = 0
        transactions = []
        if primary_group_goal.is_overall:
            transactions = Transactions.objects.filter(
            user=user_group.user,
            week__range=[primary_group_goal.start_date, primary_group_goal.end_date]  # Filter by transaction week within range
            )
        else: 
        # Get transactions related to the user and group goals
            transactions = Transactions.objects.filter(
            user=user_group.user, 
            group_goal__is_primary=True, 
            group_goal__group__in=user_groups,
            week__range=[primary_group_goal.start_date, primary_group_goal.end_date]  # Filter by transaction week within range
            )
        
        # Iterate through transactions and calculate sums based on savings or spendings
        for transaction in transactions:
            if (primary_group_goal.is_spending):
                if transaction.amount < 0:
                    total_score += transaction.amount
            else:
                if transaction.amount > 0:
                    total_score += transaction.amount
        color = None
        try:
            user_profile = UserProfile.objects.get(user=user_group.user)
            color = user_profile.color  # Get user's color from UserProfile
        except:
            pass
        # Append user's name and total score to the leaderboard
        leaderboard.append({'name': user_group.user.username, 'score': total_score, 'color': color})
    
    # Sort the leaderboard by score in descending order
    leaderboard.sort(key=lambda x: x['score'], reverse=True)
    
    context = {
        'leaderboard': leaderboard,
        'opted': opted,
        'primary_group_goal': primary_group_goal.goal_name  # Pass the primary group goal's name in the context
    }
    return render(request, 'leaderboard.html', context)

@login_required
def group_settings(request):
    # Get the current user
    user = request.user
    # Query the UserJoinGroup model to retrieve the groups the user is a part of
    user_groups = UserJoinGroup.objects.filter(user=user)
    if not user_groups:
        return redirect('groups')
    # Create a list to store the user's groups along with admin status
    user_groups_info = []
    # Iterate through the user's groups and determine if they are an admin
    members = []
    for user_group in user_groups:
        is_admin = user_group.group.admin_user == user
        user_groups_info.append({'group': user_group.group, 'is_admin': is_admin})
        members_id = UserJoinGroup.objects.filter(group=user_group.group)
        admin = user_group.group.admin_user
        group_add = user_group.group
    
    for ujg in members_id:
        members.append(ujg.user)
    # Pass the user_groups_info context variable to the template
    try:
        profile = UserProfile.objects.get(user=request.user)
    except:
        profile = None

    context = {
        'admin': admin,
        'user_groups_info': user_groups_info,
        'group': group_add,
        'members': members,
        'profile': profile,
    }
    # print(context)

    # Render the template with the context
    return render(request, 'group_settings.html', context)

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
    user_id = request.user.id
    categories = UserJoinCategory.objects.filter(user=current_user)
    group = UserJoinGroup.objects.filter(user=user_id)
    groupID = ""
    group_goals_sorted = []
    if len(group) != 0:
        for gr in group:
            groupID = gr.group.id
        group_goals = GroupGoal.objects.filter(group_id=groupID)
        for goal in group_goals:
            if not goal.is_overall:
                group_goals_sorted.append(goal)

    return render(request, "create_transaction.html", {'categories': categories, 'group_goals': group_goals_sorted})

@login_required
def create_personal_goal_page(request):
    current_user = request.user
    categories = UserJoinCategory.objects.filter(user=current_user)

    return render(request, "create_personal_goals.html", {'categories': categories})

@login_required  # Requires the user to be logged in to access this view
def create_personal_goals(request):
    print("create_personal_goals ")
    if request.method == "POST":
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
        transactions = []
        if (category):
            if (is_spending):
                transactions = Transactions.objects.filter(
                user=user,
                week__range=[goal_start_date, goal_end_date],  # Filter by transaction week within range
                amount__lt=0,
                category = category
                )
            else:
                transactions = Transactions.objects.filter(
                user=user,
                week__range=[goal_start_date, goal_end_date],  # Filter by transaction week within range
                amount__gt=0,
                category = category
                )
        else:
            if (is_spending):
                transactions = Transactions.objects.filter(
                user=user,
                week__range=[goal_start_date, goal_end_date],  # Filter by transaction week within range
                amount__lt=0
                )
            else:
                transactions = Transactions.objects.filter(
                user=user,
                week__range=[goal_start_date, goal_end_date],  # Filter by transaction week within range
                amount__gt=0
                )
        for transaction in transactions:
            personal_goal.sum_transaction += abs(transaction.amount)
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

        user_id = request.user.id
        group = UserJoinGroup.objects.filter(user=user_id)
        groupID = ""
        group_goal_id = 0
        if (len(group) != 0):  
            for gr in group:
                groupID = gr.group.id
            group_goals = GroupGoal.objects.filter(group_id=groupID)
            group_goal = request.POST.get("group_goal")
            if (group_goal == "No Group Goal"):
                group_goal_id = None
            else:
                for goal in group_goals:
                    if (goal.goal_name == group_goal):
                        group_goal_id = goal.id
        else:
            group_goal_id = None
        
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

        transaction = Transactions(
            user=user,
            week=transaction_date,  # Assuming you want to record the current date and time
            amount=amount,
            name=transaction_name,  # Provide a name for the transaction as needed
            category=category,  # Assuming category is a valid value
            group_goal_id=group_goal_id,
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
    if not UserProfile._meta.db_table in connection.introspection.table_names():
        # Create the Student table if it doesn't exist
        with connection.schema_editor() as schema_editor:
            schema_editor.create_model(UserProfile)

    result = 1
    return JsonResponse({'result': result})

@login_required
def view_transactions(request, view_all = True):
    # Ensure user is authenticated before accessing request.user
    if request.user.is_authenticated:
        current_user = request.user
        #selected_categories = request.GET.getlist('selected_categories')
        
        # Gets all transactions
        sorted = []
        username = request.user.username
        #start_date_str = request.GET.get('start_date')
        #end_date_str = request.GET.get('end_date')
        selected_categories = request.session.get('selected_categories')
        start_date_str = request.session.get('start_date_str')
        end_date_str = request.session.get('end_date_str')
        categories_list = []
        view_all = False
        view_all = request.GET.get('view_all') == 'True'
        transactions = []
        
        if False:
            transactions = Transactions.objects.all()
            print("view all???")
        else:
            categories_list = []
            if selected_categories and not selected_categories == ['']:
                categories_list = selected_categories[0].split(",")
            if start_date_str and end_date_str:
                start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
                end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
                transactions = Transactions.objects.filter(week__gte=start_date, week__lte=end_date)
            elif start_date_str:
                start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
                transactions = Transactions.objects.filter(week__gte=start_date)
            elif end_date_str:
                end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
                transactions = Transactions.objects.filter(week__lte=end_date)
            else:
                transactions = Transactions.objects.all()

        for transaction in transactions:
            # Only gets the transactions of the currently logged in user
            if (transaction.user.username == username):
                if (selected_categories and not selected_categories == ['']):
                    if (transaction.category.category_id in categories_list):
                        sorted.append(transaction)
                else:
                    sorted.append(transaction)

        categories = UserJoinCategory.objects.filter(user=current_user)

        context = {
            'transactions': sorted,
            'current_user': current_user,
            'categories': categories,
            'start_date': start_date_str,
            'end_date': end_date_str,
            'selected_categories': categories_list,
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
def home_view(request):
    current_user = request.user

    user_agent = get_user_agent(request)
    screen_width = None

    if user_agent.is_mobile:
        screen_width = 400
    elif user_agent.is_tablet:
        screen_width = 600
    else:
        screen_width = 800

    start_date_str = request.GET.get('start_date')
    end_date_str = request.GET.get('end_date')

    positive_transactions = Transactions.objects.filter(user=current_user, amount__gte=0)
    start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date() if start_date_str else None
    end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date() if end_date_str else None

    positive_transactions = Transactions.objects.filter(user=request.user, amount__gt=0)
    negative_transactions = Transactions.objects.filter(user=request.user, amount__lt=0)

    if start_date:
        positive_transactions = positive_transactions.filter(week__gte=start_date)
        negative_transactions = negative_transactions.filter(week__gte=start_date)
    if end_date:
        positive_transactions = positive_transactions.filter(week__lte=end_date)
        negative_transactions = negative_transactions.filter(week__lte=end_date)
    if not start_date and not end_date:
        end_date = timezone.now().date()
        start_date = end_date - timedelta(days=7)
        positive_transactions = positive_transactions.filter(week__range=[start_date, end_date])
        negative_transactions = negative_transactions.filter(week__range=[start_date, end_date])
        
    positive_sum = 0
    for action in positive_transactions:
        positive_sum += action.amount

    negative_sum = 0
    for action in negative_transactions:
        negative_sum += action.amount * -1

    positive_sum_str = "${:.2f}".format(positive_sum)
    negative_sum_str = "${:.2f}".format(negative_sum)

    if positive_sum >= 1000:
        positive_sum_str = "${:.2f}K".format(positive_sum / 1000)
    
    if positive_sum >= 1000000:
        positive_sum_str = "${:.2f}M".format(positive_sum / 1000000)

    if positive_sum >= 1000000000:
        positive_sum_str = "${:.2f}B".format(positive_sum / 1000000000)

    if negative_sum >= 1000:
        negative_sum_str = "${:.2f}K".format(negative_sum / 1000)
    
    if negative_sum >= 1000000:
        negative_sum_str = "${:.2f}M".format(negative_sum / 1000000)

    if negative_sum >= 1000000000:
        negative_sum_str = "${:.2f}B".format(negative_sum / 1000000000)

    return render(request, 'home.html', {'screen_width': screen_width, 'positive_sum': positive_sum_str, 'negative_sum': negative_sum_str})

@login_required
def update_home_view(request):
    current_user = request.user

    user_agent = get_user_agent(request)
    screen_width = None

    if user_agent.is_mobile:
        screen_width = 400
    elif user_agent.is_tablet:
        screen_width = 600
    else:
        screen_width = 800

    start_date_str = request.GET.get('start_date')
    end_date_str = request.GET.get('end_date')

    positive_transactions = Transactions.objects.filter(user=current_user, amount__gte=0)
    start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date() if start_date_str else None
    end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date() if end_date_str else None

    positive_transactions = Transactions.objects.filter(user=request.user, amount__gt=0)
    negative_transactions = Transactions.objects.filter(user=request.user, amount__lt=0)

    if start_date:
        positive_transactions = positive_transactions.filter(week__gte=start_date)
        negative_transactions = negative_transactions.filter(week__gte=start_date)
    if end_date:
        positive_transactions = positive_transactions.filter(week__lte=end_date)
        negative_transactions = negative_transactions.filter(week__lte=end_date)
    if not start_date and not end_date:
        end_date = timezone.now().date()
        start_date = end_date - timedelta(days=7)
        positive_transactions = positive_transactions.filter(week__range=[start_date, end_date])
        negative_transactions = negative_transactions.filter(week__range=[start_date, end_date])
        
    positive_sum = 0
    for action in positive_transactions:
        positive_sum += action.amount

    negative_sum = 0
    for action in negative_transactions:
        negative_sum += action.amount * -1

    positive_sum_str = "${:.2f}".format(positive_sum)
    negative_sum_str = "${:.2f}".format(negative_sum)

    if positive_sum > 1000:
        positive_sum_str = "${:.2f}K".format(positive_sum / 1000)
    
    if positive_sum > 1000000:
        positive_sum_str = "${:.2f}M".format(positive_sum / 1000000)

    if positive_sum > 1000000000:
        positive_sum_str = "${:.2f}B".format(positive_sum / 1000000000)

    if negative_sum > 1000:
        negative_sum_str = "${:.2f}K".format(negative_sum / 1000)
    
    if negative_sum > 1000000:
        negative_sum_str = "${:.2f}M".format(negative_sum / 1000000)

    if negative_sum > 1000000000:
        negative_sum_str = "${:.2f}B".format(negative_sum / 1000000000)
    return JsonResponse({'screen_width': screen_width, 'positive_sum': positive_sum_str, 'negative_sum': negative_sum_str})
    
@login_required
def check_user_group(request, page):
    # Ensure user is authenticated before accessing request.user
    if request.user.is_authenticated:
        username = request.user.username
        user = User.objects.get(username=username)
        is_admin = False
        if (Group.objects.filter(admin_user=user).exists()):
            is_admin = True
        # Check if there's an existing relationship between user and category
        if UserJoinGroup.objects.filter(user=user).exists():
            if page == "group_goals":
                user_join_groups = UserJoinGroup.objects.filter(user = request.user)
                for the_group in user_join_groups:
                    user_group = the_group.group
                    group_goals = GroupGoal.objects.filter(group = user_group)
                context = {
                    'goals': group_goals,
                    'is_admin': is_admin
                }
            else:
                context = {
                'is_admin': is_admin
                }
        # Render the template with the transactions data
            return render(request, page + '.html', context)
        else:
            return redirect('groups')
    else:
        # Redirect to login page if user is not authenticated
        return redirect('login')
    


@login_required  # Requires the user to be logged in to access this view
def create_group(request):
    try:
            UserJoinGroup.objects.get(user=request.user)
            return redirect('group_settings')

    except:
            # Create a new relationship between user and group
        print()
    
    group_name = request.POST.get("name")
    group_password = request.POST.get("password1")
    group_password2 = request.POST.get("password2")
    if (str(group_password) != str(group_password2)):
        messages.error(request, "Group passwords do not match")
        return render(request, 'create_groups.html')
        
    print(group_password)
    print(group_password2)
    if (group_password != group_password2):
        return render(request, 'join_groups.html')
    username = request.user.username
    user = User.objects.get(username=username)
    group = None
    existing_groups = Group.objects.filter(name=group_name).exists()
    if existing_groups:
        messages.error(request, "Group name already exists, please choose a different one.")
        return render(request, 'create_groups.html')

    '''if UserJoinGroup.objects.filter(user=user).exists():
        # any popup?
        print("eete")
        return render(request, 'group_settings.html')'''
    
    group = Group(name=group_name, admin_user=user, password=group_password)
    group.save()
    # Check if there's an existing relationship between user and group
    print(group.name)
    if group:
        try:
            print("try")
            UserJoinGroup.objects.get(user=user, group=group)
        except UserJoinGroup.DoesNotExist:
            # Create a new relationship between user and group
            user_group = UserJoinGroup(user=user, group=group)
            user_group.save()
            print("exception")
    # this causes an error when you refresh after creating the group
    # Changing to redirect instantly has error when you hit create
    return redirect('group_settings')

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
    
def view_personal_goals_test(request):
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
        return render(request, 'view_personal_goals_test.html', context)
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

        user_id = request.user.id
        group = UserJoinGroup.objects.filter(user=user_id)
        groupID = ""
        group_goal_id = 0
        if len(group) != 0:
            for gr in group:
                groupID = gr.group.id
            group_goals = GroupGoal.objects.filter(group_id=groupID)
            group_goal = request.POST.get("group_goal")
            if (group_goal == "No Group Goal"):
                group_goal_id = None
            else:
                for goal in group_goals:
                    if (goal.goal_name == group_goal):
                        group_goal_id = goal.id
        else:
            group_goal_id = None
        
        # Update the transaction object with the new data
        category = Category.objects.get(category_id=category_id)
        transaction.week = week
        transaction.amount = amount
        transaction.name = name
        transaction.category = category
        transaction.group_goal_id = group_goal_id
        transaction.save()
        return redirect('view_transactions')
    
    # Retrieve all categories for populating the dropdown
    user_id = request.user.id
    current_user = request.user
    categories = UserJoinCategory.objects.filter(user=current_user)
    is_negative = transaction.amount < 0
    if is_negative:
        transaction.amount = abs(transaction.amount)
    group = UserJoinGroup.objects.filter(user=user_id)
    group_goals_sorted = []
    groupID = ""
    if len(group) != 0:
        for gr in group:
            groupID = gr.group.id
        group_goals = GroupGoal.objects.filter(group_id=groupID)
        group_goals_sorted = []
        for goal in group_goals:
            if not goal.is_overall:
                group_goals_sorted.append(goal)
    
    return render(request, 'edit_transaction.html', {'transaction': transaction, 'categories': categories, 'is_negative': is_negative, 'group_goals': group_goals_sorted})

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
    if not start_date and not end_date:
        end_date = timezone.now().date()
        start_date = end_date - timedelta(days=7)
        negative_transactions = negative_transactions.filter(week__range=[start_date, end_date])

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
    sum = 0
    for datum in data:
        sum += float(datum)
    percentages = []
    for datum in data:
        percent = float(datum) / sum
        percent *= 100
        percentages.append(int(percent))
    for i in range(len(labels)):
        labels[i] = labels[i] + ": " + str(percentages[i]) + "%"

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
    if not start_date and not end_date:
        end_date = timezone.now().date()
        start_date = end_date - timedelta(days=7)
        positive_transactions = positive_transactions.filter(week__range=[start_date, end_date])

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
    sum = 0
    for datum in data:
        sum += float(datum)
    percentages = []
    for datum in data:
        percent = float(datum) / sum
        percent *= 100
        percentages.append(int(percent))
    for i in range(len(labels)):
        labels[i] = labels[i] + ": " + str(percentages[i]) + "%"

    chart_data = {
        'labels': labels,
        'data': data,
    }
    print(chart_data)
    return JsonResponse(chart_data)

def generate_income_line_chart(request):
    start_date_str = request.GET.get('start_date')
    end_date_str = request.GET.get('end_date')

    # Convert date strings to datetime objects
    start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date() if start_date_str else None
    end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date() if end_date_str else None

    positive_transactions = Transactions.objects.filter(user=request.user, amount__gt=0)

    if start_date:
        positive_transactions = positive_transactions.filter(week__gte=start_date)
    if end_date:
        positive_transactions = positive_transactions.filter(week__lte=end_date)
    if not start_date and not end_date:
        end_date = timezone.now().date()
        start_date = end_date - timedelta(days=7)
        positive_transactions = positive_transactions.filter(week__range=[start_date, end_date])

    aggregated_data = positive_transactions.values('week').annotate(total_amount=Sum('amount')).order_by('week')

    transaction_dict = {entry['week']: entry['total_amount'] for entry in aggregated_data}

    # Fill in missing dates with zero amounts
    if not end_date:
        end_date = timezone.now().date()
    if not start_date:
        start_date = end_date - timedelta(days=7)
    current_date = start_date
    while current_date <= end_date:
        if current_date not in transaction_dict:
            transaction_dict[current_date] = 0
        current_date += timedelta(days=1)

    sorted_transaction_dict = sorted(transaction_dict.items())

    labels = [date.strftime('%Y-%m-%d') for date, _ in sorted_transaction_dict]
    data = [amount for _, amount in sorted_transaction_dict]

    return JsonResponse({'labels': labels, 'data': data})

def generate_expenses_line_chart(request):
    start_date_str = request.GET.get('start_date')
    end_date_str = request.GET.get('end_date')

    # Convert date strings to datetime objects
    start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date() if start_date_str else None
    end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date() if end_date_str else None

    negative_transactions = Transactions.objects.filter(user=request.user, amount__lt=0)

    if start_date:
        negative_transactions = negative_transactions.filter(week__gte=start_date)
    if end_date:
        negative_transactions = negative_transactions.filter(week__lte=end_date)
    if not start_date and not end_date:
        end_date = timezone.now().date()
        start_date = end_date - timedelta(days=7)
        negative_transactions = negative_transactions.filter(week__range=[start_date, end_date])

    aggregated_data = negative_transactions.values('week').annotate(total_amount=Sum('amount')).order_by('week')

    for item in aggregated_data:    
        item['total_amount'] *= -1

    transaction_dict = {entry['week']: entry['total_amount'] for entry in aggregated_data}

    # Fill in missing dates with zero amounts
    if not end_date:
        end_date = timezone.now().date()
    if not start_date:
        start_date = end_date - timedelta(days=7)
    current_date = start_date
    while current_date <= end_date:
        if current_date not in transaction_dict:
            transaction_dict[current_date] = 0
        current_date += timedelta(days=1)

    sorted_transaction_dict = sorted(transaction_dict.items())

    labels = [date.strftime('%Y-%m-%d') for date, _ in sorted_transaction_dict]
    data = [amount for _, amount in sorted_transaction_dict]

    return JsonResponse({'labels': labels, 'data': data})

@login_required
def leave_group(request):
    # need to remove the entry in userjoingroup table    
    user = request.user
    if (Group.objects.filter(admin_user=user).exists()):
        messages.error(request, user.username + "Please first transfer ownership of your group or delete the group before deleting your account.")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    group = UserJoinGroup.objects.filter(user=user)
    if group.exists():
        group.delete()
    return redirect('groups')


@login_required
def create_group_goal_page(request):
    current_user = request.user
    group = Group.objects.filter(admin_user = current_user)
    if not group:
        return redirect('view_group_goals') 
        
    return render(request, "create_group_goal.html")

    
    
@login_required
def create_group_goal(request):
    print("create_group_goal")
    if request.method == "POST":
        print("create_group_goal POST")
        amount = float(request.POST.get("amount"))
        
        is_spending = request.POST.get("goal_type") == "on"
        is_primary = request.POST.get("is_primary") == "on"
        is_overall = request.POST.get("is_overall") == "on"
        goal_name = request.POST.get("name")
        goal_start_date = request.POST.get("start_date")
        goal_end_date = request.POST.get("end_date")
        current_user = request.user
        user_id = request.user
        # Access the user who sent the request
        user_groups = UserJoinGroup.objects.filter(user = user_id)
        groupID = ""
        group = user_groups.first().group
        username = request.user.username
        user = User.objects.get(username=username)
        
        groupPrim = UserJoinGroup.objects.filter(user=user_id).first().group
        existing_primary_goal = GroupGoal.objects.filter(group=groupPrim, is_primary=True).exists()

        if is_primary and existing_primary_goal:
            # If the group already has a primary goal, redirect with an error message
            messages.error(request, "Primary goal already exists")
            return render(request, "create_group_goal.html", {'error_message': "You already have a primary goal!"})

        group_goal = GroupGoal(
            group=group,
            amount=amount,
            goal_name=goal_name,  # Provide a name for the transaction as needed
            sum_transaction = 0,
            is_spending = is_spending,
            start_date = goal_start_date,
            end_date = goal_end_date,
            is_overall = is_overall,
            is_primary = is_primary
        )
        all_users = UserJoinGroup.objects.filter(group=group).select_related('user')
        print("ALL USERS")
        print(all_users)
    # Iterate through each user
    for user_group in all_users:
        # Initialize variables to store transaction amounts for savings and spendings
        total_score = 0
        transactions = []
        if (is_overall):
            if (is_spending):
                transactions = Transactions.objects.filter(
                user=user_group.user,
                week__range=[goal_start_date, goal_end_date],  # Filter by transaction week within range
                amount__lt=0,
                )
                print("category existed, was spending")
            else:
                transactions = Transactions.objects.filter(
                user=user_group.user,
                week__range=[goal_start_date, goal_end_date],  # Filter by transaction week within range
                amount__gt=0,
                )
                print("category existed, was savings")
        
        for transaction in transactions:
            group_goal.sum_transaction += abs(transaction.amount)
    group_goal.save()
    return redirect('view_group_goals')

def join_groups(request):
    # Ensure user is authenticated before accessing request.user
    if request.user.is_authenticated:
        try:
            print("try")
            UserJoinGroup.objects.get(user=request.user)
            return redirect('group_settings')
        except:
            # Create a new relationship between user and group
            print()
        current_user = request.user

        # selected_categories = request.GET.getlist('selected_categories')
        # print("---------")
        # print(selected_categories)
        # print("---------")
        
        # Gets all transactions
        sorted = []
        username = request.user.username


        groups = Group.objects.all()
        search = request.POST.get("search_input", "").lower()
        if search == "":
            sorted = groups
        else:
            for group in groups:
                # Only gets the transactions of the currently logged in user
                if search in group.name.lower():
                    sorted.append(group)

        context = {
            'groups': sorted,
            'current_user': current_user,
        }
        
        # Render the template with the transactions data
        return render(request, 'join_groups.html', context)
    else:
        # Redirect to login page if user is not authenticated
        return redirect('login')

def join_group_action(request, group_id):
    if request.user.is_authenticated:

        group = Group.objects.get(id=group_id)
        if group.password == "":
            public = True
        else:
            public = False
        context = {
            'public': public,
            'group': group,
        }
        return render(request, 'join_specific_group.html', context)
    else:
        # Redirect to login page if user is not authenticated
        return redirect('login')
    
def join_specific_group_action(request, group_id):
    if request.user.is_authenticated:
        group_password = request.POST.get("password")
        try:
            UserJoinGroup.objects.get(user=request.user)
            return redirect('group_settings')
        except:
            # Create a new relationship between user and group
            print()
        username = request.user.username
        user = User.objects.get(username=username)
        group = Group.objects.get(id=group_id)
        group_password = request.POST.get("password")

        if group_password == None:
            group_password = ""
        print("-" + group_password + "-")
        print("-" + group.password + "-")
        if (group_password != group.password):
            print("testing")
            messages.error(request, "Invalid Group Password.")
            return redirect('join_group_action', group_id=group.id)

        user_to_group = UserJoinGroup(user=user, group=group)
        user_to_group.save()

        # this causes an error when you refresh after creating the group
        # Changing to redirect instantly has error when you hit create
        return redirect('group_settings')
    else:
        # Redirect to login page if user is not authenticated
        return redirect('login')

@login_required
def promote_to_admin(request, userToPromote):
    if request.user.is_authenticated:
        new_admin = User.objects.get(id=userToPromote)
        group = Group.objects.get(admin_user=request.user)
        if group == None:
            return redirect('group_settings')
        group.admin_user = new_admin
        group.save()
        return redirect('group_settings')
    else:
        # Redirect to login page if user is not authenticated
        return redirect('login')

@login_required
def remove_member(request, userToRemove):
    if request.user.is_authenticated:
        user_to_remove = User.objects.get(id=userToRemove)
        group = Group.objects.get(admin_user=request.user)
        if group == None:
            return redirect('group_settings')
        if user_to_remove == group.admin_user:
            return redirect('group_settings')
        to_remove = UserJoinGroup.objects.get(user=user_to_remove)
        to_remove.delete()
        return redirect('group_settings')
    else:
        # Redirect to login page if user is not authenticated
        return redirect('login')

def edit_group_goal_action(request, goal_id):
    goal = get_object_or_404(GroupGoal, pk=goal_id)
    if request.method == 'POST':
        # Retrieve the form data from the POST request
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        amount = request.POST.get('amount')
        name = request.POST.get('name')
        #category_id = request.POST.get('type')
        is_spending = request.POST.get("goal_type") == "on"
        is_primary = request.POST.get("is_primary") == "on"
        if is_primary and GroupGoal.objects.filter(is_primary=True).exclude(pk=goal_id).exists():
            # Another primary goal already exists, show alert and redirect back
            messages.error(request, 'Another primary goal already exists. You cannot set this goal as primary.')
            return render(request, 'edit_group_goal.html', {'goal': goal, 'is_primary': goal.is_primary, 'is_overall': goal.is_overall, 'is_spending': goal.is_spending})
           # return render(request, 'edit_group_goal_action')
            
        is_overall = request.POST.get("is_overall") == "on"
    
        if is_spending:
            amount = str(float(amount) * -1)
       # category = Category.objects.get(category_id=category_id)
        goal.start_date = start_date
        goal.end_date = end_date
        goal.amount = amount
        goal.goal_name = name
        #goal.category= category
        goal.is_spending = is_spending
        goal.is_primary = is_primary
        goal.is_overall = is_overall
        goal.save()

        #messages.success(request, 'Another primary goal already exists. You cannot set this goal as primary.')
        #return render(request, 'view_group_goals', {'goal': goal, 'is_primary': goal.is_primary, 'is_overall': goal.is_overall, 'is_spending': goal.is_spending, 'error_message': '', 'goal_id': goal_id})
        return redirect('view_group_goals')
    
    # Retrieve all categories for populating the dropdown
    user_id = request.user.id
    current_user = request.user
    
    is_spending = goal.is_spending
    if goal.is_spending:
        goal.amount = abs(goal.amount)
    
    is_primary = goal.is_primary
    is_overall = goal.is_overall
    
    
    
    
    
    
    return render(request, 'edit_group_goal.html', {'goal': goal, 'is_primary': is_primary, 'is_overall':is_overall, 'is_spending': goal.is_spending})

def delete_group_goal(request, goal_id):
    if request.method == 'POST':
        goal = GroupGoal.objects.get(pk=goal_id)
        goal.delete()
        return JsonResponse({'message': 'Goal deleted successfully.'})
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=400)

@login_required
def update_toggle(request):

    if request.method == 'POST':
        data = json.loads(request.body)
        isChecked = data['isChecked']
        
        try:
            profile = UserProfile.objects.get(user=request.user)
        except:
            profile = UserProfile.objects.create(user=request.user)
        
        profile.opt_in = isChecked
        profile.save()

        return JsonResponse({'message': 'Toggle updated successfully'})
    else:
        return JsonResponse({'error': 'Invalid request method'})
    
@login_required
def update_subscribe(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        isChecked = data.get('isChecked', False)  # Default to False if not provided

        # Get the current user
        user = request.user
        if isChecked:
            # Check if the user is already subscribed
            if not SubscriberList.objects.filter(user=user).exists():
                # If not subscribed, add the user to the SubscriberList
                SubscriberList.objects.create(user=user)
            send_mail(
                f"Subscribed to Weekly Subscription Email",
                "You have successfully subscribed to our weekly email updates!",
                settings.EMAIL_HOST_USER,
                [user.email],  # Sending email to the user's email address
                fail_silently=False
                )
        else:
            # If isChecked is False, remove the user from SubscriberList if they are on it
            SubscriberList.objects.filter(user=user).delete()
            send_mail(
                f"Unsubscribed from Weekly Subscription Email",
                "You have successfully unsubscribed from our weekly email updates!",
                settings.EMAIL_HOST_USER,
                [user.email],  # Sending email to the user's email address
                fail_silently=False
                )

        return JsonResponse({'message': 'Subscription preferences updated successfully'})
    else:
        return JsonResponse({'error': 'Invalid request method'})