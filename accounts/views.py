from django.shortcuts import render

# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import CreateView


# class SignUpView(CreateView):
#     form_class = UserCreationForm
#     success_url = reverse_lazy("login")
#     template_name = "registration/signup.html"

from django.shortcuts import render
from django.contrib.auth import login, authenticate
from .forms import SignUpForm
from django.shortcuts import render, redirect
from my_app.models import UserJoinCategory, Category
from django.http import JsonResponse
from django.http import HttpResponseRedirect

def home_view(request):
    return render(request, 'home.html')

def initialize_database_for_user(user):
    categories = ["Groceries", "Transportation", "Entertainment", "Shopping", "Housing", "Utilities", "Insurance", "Dining"]
    for category_name in categories:
        category = None
        try:
            category = Category.objects.get(category_id=category_name)
        except Category.DoesNotExist:
            # Create a new category
            print("Creating category" + category_name)
            category = Category(category_id=category_name)
            category.save()
        user_category = UserJoinCategory(user=user, category=category)
        user_category.save()

def signup(request):
    if request.user.is_anonymous:
        if request.method == 'POST':
            form = SignUpForm(request.POST)
            if form.is_valid():
                new_user = form.save()
                initialize_database_for_user(new_user)
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password1')
                user = authenticate(username=username, password=password)
                login(request, user)
                print("success")
                return JsonResponse({'success': True})
            else:
                # Form validation failed
                errors = dict(form.errors.items())
                return JsonResponse({'success': False, 'errors': errors})
        else:
            form = SignUpForm()
        return render(request, 'registration/signup.html', {'form': form})
    else:
        return render(request, 'home.html')