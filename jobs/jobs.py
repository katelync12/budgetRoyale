from django.conf import settings
import requests
import json
import random
#python manage.py runserver --noreload
from my_app.models import *
from my_app.views import send_subscription_email
from django.core.management import call_command


def cleanup():
    try:
        call_command('clearsessions')
    except Exception as e:
        print(f"An error occurred in schedule_api: {e}")


def schedule_api():
    #print("Hello, world!")
    try:
        subscribers = SubscriberList.objects.all()
        for subscriber in subscribers:
            print(subscriber.user.id)
            send_subscription_email(subscriber.user.id)
    except Exception as e: 
        print(f"An error occurred in schedule_api: {e}")
