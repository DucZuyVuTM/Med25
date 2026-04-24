from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser
from patients.models import Patient


@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if not created:
        return

    if instance.role == 'patient':
        Patient.objects.create(
            user=instance,
            surname='',
            name='',
            phone='',
            address='',
        )
    # Doctor and Administrator were created manually by the admin
    # because more specialized information was needed
