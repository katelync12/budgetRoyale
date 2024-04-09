from django.conf import settings
import requests
import json
import random
#python manage.py runserver --noreload
from my_app.models import *


def schedule_api():
    print("Hello, world!")
    subscribers = SubscriberList.objects.all()
    for subscriber in subscribers:
        print(subscriber.user.id)
        '''postcode = postcodes[random.randint(0, 3)]

        full_url = f"https://api.postcodes.io/postcodes/{postcode}"
                
        r = requests.get(full_url)
        if r.status_code == 200:

            result = r.json()["result"]

            lat = result["latitude"]
            lng = result["longitude"]

            print(f'Latitude: {lat}, Longitude: {lng}')'''
