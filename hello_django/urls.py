"""
URL configuration for hello_django project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
# imported views
from my_app import views
from django.views.generic.base import TemplateView
from django.contrib.auth import views as auth_views


urlpatterns = [
    # path('add/', views.add, name='add'),
    # path('', views.home, name="homepage"),
    
      # configured the url
    # path('index/', views.index, name="homepage1"),

    # path("", include("my_app.urls")),
    path('create_transaction/', views.create_transaction, name='create_transaction'),
    path('transactions/', views.view_transactions, name='transactions'),
    path('admin/', admin.site.urls),
    path('create_data/', views.add, name='create_data'),
    path("accounts/", include("accounts.urls")),
    path("accounts/", include("django.contrib.auth.urls")),
    path("", TemplateView.as_view(template_name="home.html"), name="home"),
    # path("", TemplateView.as_view(template_name="registration/login.html"), name="login"),
    path("form/", TemplateView.as_view(template_name="form.html"), name="form"),
    path("personal-goals/", TemplateView.as_view(template_name="view_personal_goals.html"), name="view_personal_goals"),
    path("groups/", TemplateView.as_view(template_name="groups.html"), name="groups"),
    path("transactions/", TemplateView.as_view(template_name="view_transactions.html"), name="view_transactions"),
    path("transactions/create/", views.create_transaction_page, name="create_transactions"),
    path('login/', views.login_view, name='login'),
    path('add_category/', views.add_category, name='add_category')
]
