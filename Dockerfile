FROM python:3
RUN pip install django==3.2 psycopg2 psycopg2-binary python-decouple django-pgtrigger
COPY . .
RUN python manage.py migrate
CMD ["python","manage.py","runserver","0.0.0.0:80"]
