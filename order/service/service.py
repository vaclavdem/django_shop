from django.core.mail import send_mail


def send_ultimative_mail(title, text, user_email):
    send_mail(
        title,
        text,
        'cy4ok2006@gmail.com',
        [user_email],
    )



