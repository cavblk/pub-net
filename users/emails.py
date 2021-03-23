from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.shortcuts import reverse


def send_register_email(user):
    context = {
        'first_name': user.first_name,
        'last_name': user.last_name,
        'login_url': f"http://localhost:8000/{reverse('users:login')}",
    }
    template = get_template('users/emails/register.html')
    content = template.render(context)

    mail = EmailMultiAlternatives(
        subject='Your account have been registered.',
        body=content,
        from_email='vladuomihai@gmail.com',
        to=[user.email]
    )
    mail.content_subtype = 'html'
    mail.send()
