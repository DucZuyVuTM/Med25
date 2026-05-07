from django.db import models

# Create your models here.
class Schedule(models.Model):
    """The appointment schedule is created by the administrator
    - specifying the time slot and location for the examination."""

    administrator = models.ForeignKey(
        'accounts.Administrator',
        on_delete=models.PROTECT,
        related_name='schedules',
        verbose_name='Administrator',
    )
    reception_start_time = models.DateTimeField(verbose_name='Reception start date and time')
    reception_end_time = models.DateTimeField(verbose_name='Reception end date and time')
    reception_place = models.TextField(verbose_name='Reception location')

    class Meta:
        verbose_name = 'Schedule'
        verbose_name_plural = 'Schedules'
        ordering = ['reception_start_time']

    def __str__(self):
        return f'Schedule {self.reception_start_time} - {self.reception_place}'


class Reception(models.Model):
    """Reception - the hub table that connects
    doctors, equipment, patients, schedules, and documents."""

    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('no_show', 'Absent'),
    ]

    doctor = models.ForeignKey(
        'accounts.Doctor',
        on_delete=models.PROTECT,
        related_name='receptions',
        verbose_name='Doctor',
    )
    clinic_equipment = models.ForeignKey(
        'equipment.ClinicEquipment',
        on_delete=models.PROTECT,
        related_name='receptions',
        verbose_name='Clinic equipment',
    )
    medical_card = models.ForeignKey(
        'patients.MedicalCard',
        on_delete=models.PROTECT,
        related_name='receptions',
        verbose_name='Medical record',
    )
    patient = models.ForeignKey(
        'accounts.CustomUser',
        on_delete=models.PROTECT,
        related_name='receptions',
        verbose_name='Patient',
    )
    document = models.ForeignKey(
        'documents.Document',
        on_delete=models.PROTECT,
        related_name='receptions',
        verbose_name='Document',
    )
    schedule = models.ForeignKey(
        Schedule,
        on_delete=models.PROTECT,
        related_name='receptions',
        verbose_name='Schedule',
    )
    result = models.TextField(verbose_name='Reception result')
    prescription = models.TextField(verbose_name='Prescription')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='scheduled', verbose_name='Status')

    class Meta:
        verbose_name = 'Reception'
        verbose_name_plural = 'Receptions'
        ordering = ['-schedule__reception_start_time']

    def __str__(self):
        return (
            f'Reception #{self.pk} - {self.patient} '
            f'| Dr. {self.doctor.employee.full_name} '
            f'| {self.schedule.reception_date}'
        )
