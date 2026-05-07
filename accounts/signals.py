from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser, Employee, Doctor, Administrator, Position


@receiver(post_save, sender=CustomUser)
def create_employee_for_staff(sender, instance, created, **kwargs):
    """
    Automatically create Employee profile when a user with role 
    'doctor' or 'administrator' is created.
    """
    if created and instance.role in ['doctor', 'administrator']:
        # Create employee with placeholder data
        # Admin should update these fields later
        from django.utils import timezone
        
        # Get or create a default position (you should create this via migration)
        default_position, _ = Position.objects.get_or_create(
            title='New Position',
            defaults={
                'salary': 0,
                'access_category': 'Pending setup',
            }
        )
        
        Employee.objects.create(
            user=instance,
            position=default_position,
            employment_date=timezone.now().date(),
            contract_end_date=timezone.now().date() + timezone.timedelta(days=365),
        )


@receiver(post_save, sender=Employee)
def create_doctor_or_admin_profile(sender, instance, created, **kwargs):
    """
    Automatically create Doctor or Administrator profile when Employee is created.
    """
    if created:
        if instance.user.role == 'doctor':
            Doctor.objects.get_or_create(
                employee=instance,
                defaults={
                    'specialty': 'To be updated',
                    'work_experience': 'To be updated',
                }
            )
        elif instance.user.role == 'administrator':
            Administrator.objects.get_or_create(
                employee=instance,
                defaults={
                    'system_access_rights': 'To be updated',
                }
            )
