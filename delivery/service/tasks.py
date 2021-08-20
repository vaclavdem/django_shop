from django_shop.celery import app
from .service import send_ultimative_mail


@app.task
def send_email(title, text, user_email):
    send_ultimative_mail(title, text, user_email)
