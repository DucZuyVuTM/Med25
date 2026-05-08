from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import CustomUser, Employee, Doctor, Administrator, Position


@receiver(pre_save, sender=CustomUser)
def detect_role_change(sender, instance, **kwargs):
    if instance.pk:
        try:
            old_instance = CustomUser.objects.get(pk=instance.pk)
            instance._old_role = old_instance.role
        except CustomUser.DoesNotExist:
            instance._old_role = None
    else:
        instance._old_role = None


@receiver(post_save, sender=CustomUser)
def create_employee_for_staff(sender, instance, created, **kwargs):
    should_create = False

    if created and instance.role in ['doctor', 'administrator']:
        should_create = True
    elif (
        hasattr(instance, '_old_role')
        and instance._old_role != instance.role
        and instance.role in ['doctor', 'administrator']
    ):
        should_create = True

    if should_create:
        from django.utils import timezone

        default_position, _ = Position.objects.get_or_create(
            title='New Position',
            defaults={
                'salary': 0,
                'access_category': 'Pending setup',
            }
        )

        Employee.objects.get_or_create(
            user=instance,
            defaults={
                'position': default_position,
                'employment_date': timezone.now().date(),
                'contract_end_date': timezone.now().date() + timezone.timedelta(days=365),
            }
        )


@receiver(post_save, sender=CustomUser)
def remove_profile_on_role_change(sender, instance, created, **kwargs):
    """
    Remove Doctor or Administrator when the role changes from that position.
    """
    if created:
        return

    old_role = getattr(instance, '_old_role', None)
    new_role = instance.role

    if old_role == new_role:
        return

    if old_role == 'doctor':
        try:
            employee = instance.employee_profile
            Doctor.objects.filter(employee=employee).delete()
        except Employee.DoesNotExist:
            pass

    elif old_role == 'administrator':
        try:
            employee = instance.employee_profile
            Administrator.objects.filter(employee=employee).delete()
            if instance.is_staff:
                CustomUser.objects.filter(pk=instance.pk).update(is_staff=False)
        except Employee.DoesNotExist:
            pass


@receiver(post_save, sender=Employee)
def create_doctor_or_admin_profile(sender, instance, created, **kwargs):
    if not created:
        return

    if instance.user.role == 'doctor':
        Doctor.objects.get_or_create(
            employee=instance,
            defaults={
                'speciality': 'To be updated',
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


@receiver(post_save, sender=CustomUser)
def set_staff_status(sender, instance, created, **kwargs):
    if instance.role == 'administrator' and not instance.is_staff:
        CustomUser.objects.filter(pk=instance.pk).update(is_staff=True)

    elif instance.role != 'administrator' and instance.is_staff and not instance.is_superuser:
        CustomUser.objects.filter(pk=instance.pk).update(is_staff=False)
