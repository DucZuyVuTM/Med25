from django.db import models
from accounts.models import CustomUser

# Create your models here.
class Email(models.Model):
    """Email flow between an administrator and a patient."""

    STATUS_CHOICES = [
        ('open', 'Open'),
        ('closed', 'Closed'),
        ('pending', 'Pending'),
    ]

    administrator = models.ForeignKey(
        'accounts.Administrator',
        on_delete=models.PROTECT,
        related_name='email_threads',
        verbose_name='Administrator',
    )
    patient = models.ForeignKey(
        CustomUser,
        on_delete=models.PROTECT,
        related_name='email_threads',
        verbose_name='Patient',
        limit_choices_to={'role': 'patient'},
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='open', verbose_name='Status')

    class Meta:
        verbose_name = 'Email flow'
        verbose_name_plural = 'Email flows'
        ordering = ['-id']

    def __str__(self):
        return f'Email #{self.pk} - {self.patient} [{self.get_status_display()}]'


class Message(models.Model):
    """A specific message in the email flow."""

    SENDER_TYPE_CHOICES = [
        ('admin', 'Administrator'),
        ('patient', 'Patient'),
    ]

    email = models.ForeignKey(
        Email,
        on_delete=models.CASCADE,
        related_name='messages',
        verbose_name='Email flow',
    )
    content = models.TextField(verbose_name='Content')
    send_date = models.DateField(verbose_name='Send date')
    send_time = models.TimeField(verbose_name='Send time')
    sender_type = models.CharField(max_length=20, choices=SENDER_TYPE_CHOICES, verbose_name='Sender type')

    class Meta:
        verbose_name = 'Message'
        verbose_name_plural = 'Messages'
        ordering = ['send_date', 'send_time']

    def __str__(self):
        return f'[{self.get_sender_type_display()}] {self.send_date} {self.send_time}'
