FROM python:3
RUN pip install django==3.2 psycopg2 psycopg2-binary python-decouple django-pgtrigger APScheduler django-user-agents
COPY . .
ENV PYTHONUNBUFFERED=1
CMD ["python","manage.py","runserver","0.0.0.0:80"]
