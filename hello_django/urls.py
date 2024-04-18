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
    # path('index/ ', views.index, name="homepage1"),

    # path("", include("my_app.urls")),
    # path('edit_transaction/', views.edit_transaction, name='edit_transaction_action'),
    path('groups/spendings_breakdown/', views.spendings_breakdown, name="spendings_breakdown"),
    path('groups/spendings_chart/', views.spendings_chart, name="spendings_chart"),
    path('create_transaction/', views.create_transaction, name='create_transaction_action'),
    path('create_group/', views.create_group, name='create_group_action'),
    # path('groups/', views.groups, name='search_group_action'),
    path('create_personal_goal/', views.create_personal_goals, name='create_personal_goal_action'),
    path('delete_transaction/<int:transaction_id>/', views.delete_transaction, name='delete_transaction'),

    path('delete_goal/<int:goal_id>/', views.delete_goal, name='delete_goal'),
    path('transactions/', views.view_transactions, name='transactions'),
    path('admin/', admin.site.urls),
    path('create_data/', views.add, name='create_data'),
    path("accounts/", include("accounts.urls")),
    path("accounts/", include("django.contrib.auth.urls")),
    path("", views.home_view, name="home"),
    path("form/", TemplateView.as_view(template_name="form.html"), name="form"),
    path("send_form/", views.send_form, name="send_form"),
    path("delete_account/", views.delete_account, name="delete_account"),
    path("form_confirm/", TemplateView.as_view(template_name="form_confirm.html"), name="form_confirm"),
    path("personal-goals/", views.view_personal_goals, name="view_personal_goals"),
    path("personal-goals-test/", views.view_personal_goals_test, name="view_personal_goals_test"),
    
    path("personal-goals/create/", views.create_personal_goal_page, name="create_personal_goals"),

    path("edit_personal_goal/", TemplateView.as_view(template_name="edit_personal_goal.html"), name="edit_personal_goal_view"),
    path("edit_personal_goal/<int:goal_id>/", views.edit_personal_goal_action, name="edit_personal_goal_action"),

    path("groups/create/", TemplateView.as_view(template_name="create_groups.html"), name="create_groups"),


    path('groups/join/<int:group_id>/', views.join_group_action, name='join_group_action'),
    path('join_specific_group/<int:group_id>/', views.join_specific_group_action, name='join_specific_group_action'),

    path('groups/join/<int:group_id>/', views.join_group_action, name='join_group_action'),
    path('groups/join/<int:group_id>/<str:password>/', views.join_group_from_link, name='join_group_from_link'),

    path('join_specific_group/<int:group_id>/', views.join_specific_group_action, name='join_specific_group_action'),

    path("groups/leaderboard/", views.group_leaderboard, name="group_leaderboard"),
    
    # Matches groups/leave/
    path("groups/leave/", views.leave_group, name="leave_group"),
    path("groups/delete/<int:group_id>/", views.delete_group, name="delete_group"),
    path("groups/group_settings/", views.group_settings, name="group_settings"),
    #path("e", views.group_settings, name="group_settings"),
    path('promote_to_admin/<int:userToPromote>/', views.promote_to_admin, name='promote_to_admin'),
    path('remove_member/<int:userToRemove>/', views.remove_member, name='remove_member'),

    path('update_toggle/', views.update_toggle, name='update_toggle'),
    path('update_subscribe/', views.update_subscribe, name='update_subscribe'),

    # Matches groups/<str:page>/
    path("groups/<str:page>/", views.check_user_group, name="check_user_group"),
    path('groups/group_goals/create/', views.create_group_goal_page, name="create_group_goal"),
    path("groups/group_goals/", views.view_group_goals, name="view_group_goals"),
    # Matches groups/
    path("groups/", views.join_groups, name="groups"),
    
    # Matches groups/settings/
    path('add_session_filter/', views.add_session_filter, name='add_session_filter'),
    path('clear4_session_filter/', views.clear_session_filter, name='clear_session_filter'),   
    path("edit_transaction/", TemplateView.as_view(template_name="edit_transaction.html"), name="edit_transactions_view"),
    path("edit_transaction/<int:transaction_id>/", views.edit_transaction_action, name="edit_transaction_action"),
    path('update_profile_color/', views.update_profile_color, name='update_profile_color'),
    path("settings/", views.profile_settings, name="profile_settings"),
    path("transactions/", TemplateView.as_view(template_name="view_transactions.html"), name="view_transactions"),
    path("transactions/create/", views.create_transaction_page, name="create_transactions"),
    path('login/', views.login_view, name='login'),
    path('accounts/logout/', views.logout, name='logout'),
    path('add_category/', views.add_category, name='add_category'),
    path('verify_unique_category/', views.verify_unique_category, name='verify_unique_category'),
    path('generate_expenses_pie_chart/', views.generate_expenses_pie_chart, name='generate_expenses_pie_chart'),
    path('generate_income_pie_chart/', views.generate_income_pie_chart, name='generate_income_pie_chart'),
    path('generate_income_line_chart/', views.generate_income_line_chart, name='generate_income_line_chart'),
    path('generate_expenses_line_chart/', views.generate_expenses_line_chart, name='generate_expenses_line_chart'),
    path('category_chart/', views.category_chart, name='category_chart'),
    path('update_home_view/', views.update_home_view, name='update_home_view'),

    path('create_group_goal/', views.create_group_goal, name='create_group_goal_action'),

    path("edit_group_goal/", TemplateView.as_view(template_name="edit_group_goal.html"), name="edit_group_goal_view"),
    path("edit_group_goal/<int:goal_id>/", views.edit_group_goal_action, name="edit_group_goal_action"),
    path('delete_group_goal/<int:goal_id>/', views.delete_group_goal, name='delete_group_goal'),

]
