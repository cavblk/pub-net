from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.shortcuts import reverse
from utils.constants import ACTIVATION_AVAILABILITY


def send_register_email(user):
    context = {
        'first_name': user.first_name,
        'last_name': user.last_name,
        'login_url': f"http://localhost:8000{reverse('users:account:login')}",
    }
    template = get_template('users/emails/register.html')
    content = template.render(context)

    mail = EmailMultiAlternatives(
        subject='Your account have been registered.',
        body=content,
        to=[user.email]
    )
    mail.content_subtype = 'html'
    mail.send()


def send_activation_email(activation):
    user = activation.user
    context = {
        'first_name': user.first_name,
        'last_name': user.last_name,
        'activation_url': f"http://localhost:8000{reverse('users:activation:activate', args=(activation.token,))}",
        'activation_value': ACTIVATION_AVAILABILITY['value'],
        'activation_unit': ACTIVATION_AVAILABILITY['unit'],
    }
    template = get_template('users/emails/activate.html')
    content = template.render(context)

    mail = EmailMultiAlternatives(
        subject='Your account have been created.',
        body=content,
        to=[user.email]
    )
    mail.content_subtype = 'html'
    mail.send()
