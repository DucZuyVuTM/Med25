from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('patient', 'Patient'),
        ('doctor', 'Doctor'),
        ('administrator', 'Administrator'),
    ]
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        blank=True,
        verbose_name='Role',
    )

    class Meta:
        verbose_name = 'Account'
        verbose_name_plural = 'Account'

    def __str__(self):
        return f'{self.username} ({self.get_role_display()})'


class Position(models.Model):
    """Employee job title, along with salary and access permissions."""

    title = models.CharField(max_length=100, verbose_name='Job title')
    salary = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Salary')
    access_category = models.CharField(max_length=500, verbose_name='Access permissions list')

    class Meta:
        verbose_name = 'Position'
        verbose_name_plural = 'Positions'
        ordering = ['title']

    def __str__(self):
        return self.title


class Employee(models.Model):
    """Clinic staff. This could be a doctor or an administrator."""

    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='employee_profile',
        verbose_name='Profile',
    )
    position = models.ForeignKey(
        Position,
        on_delete=models.PROTECT,
        related_name='employees',
        verbose_name='Position',
    )
    manager = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='subordinates',
        verbose_name='Direct manager',
    )
    surname = models.CharField(max_length=50, verbose_name='Surname')
    name = models.CharField(max_length=50, verbose_name='Name')
    patronymic = models.CharField(max_length=50, blank=True, verbose_name='Patronymic')
    phone = models.CharField(max_length=20, unique=True, verbose_name='Phone number')
    address = models.TextField(verbose_name='Address')
    employment_date = models.DateField(verbose_name='Employment date')
    end_date_of_the_contract = models.DateField(verbose_name='Contract end date')

    class Meta:
        verbose_name = 'Employee'
        verbose_name_plural = 'Employees'
        ordering = ['surname', 'name']

    def __str__(self):
        return f'{self.surname} {self.name} {self.patronymic}'.strip()

    @property
    def full_name(self):
        return str(self)


class Doctor(models.Model):
    """Doctor - an extended profile for Employee."""

    employee = models.OneToOneField(
        Employee,
        on_delete=models.CASCADE,
        related_name='doctor_profile',
        verbose_name='Employee',
    )
    speciality = models.TextField(verbose_name='Speciality')
    work_experience = models.TextField(verbose_name='Work experience')

    class Meta:
        verbose_name = 'Doctor'
        verbose_name_plural = 'Doctors'

    def __str__(self):
        return f'Dr. {self.employee.full_name} - {self.speciality}'


class Administrator(models.Model):
    """Administrator - an extended profile for Employee."""

    employee = models.OneToOneField(
        Employee,
        on_delete=models.CASCADE,
        related_name='administrator_profile',
        verbose_name='Employee',
    )
    system_access_rights = models.CharField(max_length=500, verbose_name='System access rights')
    last_login_date = models.DateField(verbose_name='Last login')

    class Meta:
        verbose_name = 'Administrator'
        verbose_name_plural = 'Administrators'

    def __str__(self):
        return f'Admin: {self.employee.full_name}'
