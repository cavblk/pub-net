from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from users.models import Profile, Activation
from users.emails import send_activation_email

AuthUserModel = get_user_model()


@receiver(post_save, sender=AuthUserModel)
def create_profile(instance, created, **kwargs):
    if created:
        Profile(user=instance).save()


@receiver(pre_save, sender=AuthUserModel)
def inactivate_user(instance, **kwargs):
    if not instance.pk and not instance.is_social_auth:
        instance.is_active = False
        instance.password = None


@receiver(post_save, sender=AuthUserModel)
def set_activation_details(instance, created, **kwargs):
    if created:
        activation = Activation(user=instance)
        activation.save()

        send_activation_email(activation)
