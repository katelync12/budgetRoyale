from django.shortcuts import render

# Create your views here.
from django.contrib.auth.forms import UserCreationForm
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

def home_view(request):
    return render(request, 'home.html')

def initialize_database_for_user(user):
    category = Category(category_id="Food")
    user_category = UserJoinCategory(user=user, category=category)
    user_category.save()

def signup(request):
    print("signup")
    if request.user.is_anonymous:
        form = SignUpForm(request.POST)
        if form.is_valid():
            print("form is valid")
            new_user = form.save()
            initialize_database_for_user(new_user)
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('home')
        else:
            form = SignUpForm()
        return render(request, 'registration/signup.html', {'form': form})
    else:
        return render(request, 'home.html')