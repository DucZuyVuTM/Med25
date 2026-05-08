from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models


class CustomUser(AbstractUser):
    """Custom user model with role-based authentication."""

    ROLE_CHOICES = [
        ('patient', 'Patient'),
        ('doctor', 'Doctor'),
        ('administrator', 'Administrator'),
    ]

    # Role and basic info
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='patient',
        verbose_name='Role',
    )

    # Personal information (common for all users)
    patronymic = models.CharField(
        max_length=50,
        blank=True,
        verbose_name='Patronymic',
    )

    phone = models.CharField(
        max_length=20,
        validators=[
            RegexValidator(
                regex=r'^\+?[0-9\s\-\(\)]{10,20}$',
                message='Enter a valid phone number (10-20 digits, can include +, -, spaces).',
            )
        ],
        verbose_name='Phone number',
    )
    address = models.TextField(verbose_name='Address')

    class Meta:
        verbose_name = 'Account'
        verbose_name_plural = 'Accounts'
        ordering = ['first_name', 'last_name']

    def __str__(self):
        return f'{self.first_name} {self.last_name} ({self.get_role_display()})'

    @property
    def full_name(self):
        """Return full name (last_name + first_name + patronymic)."""
        name_parts = [self.last_name, self.first_name]
        if self.patronymic:
            name_parts.append(self.patronymic)
        return ' '.join(name_parts)

    def is_patient(self):
        """Check if user has patient role."""
        return self.role == 'patient'

    def is_doctor(self):
        """Check if user has doctor role."""
        return self.role == 'doctor'

    def is_administrator(self):
        """Check if user has administrator role."""
        return self.role == 'administrator'


class Position(models.Model):
    """Employee job title with salary and access permissions."""

    title = models.CharField(max_length=100, verbose_name='Job title')
    salary = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name='Salary',
    )
    access_category = models.CharField(
        max_length=500,
        verbose_name='Access permissions list',
    )

    class Meta:
        verbose_name = 'Position'
        verbose_name_plural = 'Positions'
        ordering = ['title']

    def __str__(self):
        return self.title


class Employee(models.Model):
    """Clinic staff (doctor or administrator)."""

    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='employee_profile',
        verbose_name='Profile',
        limit_choices_to={'role__in': ['doctor', 'administrator']},
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
    employment_date = models.DateField(verbose_name='Employment date')
    contract_end_date = models.DateField(verbose_name='Contract end date')

    class Meta:
        verbose_name = 'Employee'
        verbose_name_plural = 'Employees'
        ordering = ['user__last_name', 'user__first_name']

    def __str__(self):
        return self.user.full_name

    @property
    def full_name(self):
        """Return employee's full name from associated user."""
        return self.user.full_name

    @property
    def is_contract_valid(self):
        """Check if contract is still valid."""
        from django.utils import timezone
        return self.contract_end_date >= timezone.now().date()


class Doctor(models.Model):
    """Extended profile for doctors."""

    employee = models.OneToOneField(
        Employee,
        on_delete=models.CASCADE,
        related_name='doctor_profile',
        verbose_name='Employee',
        limit_choices_to={'user__role': 'doctor'},
    )
    speciality = models.TextField(verbose_name='speciality')
    work_experience = models.TextField(verbose_name='Work experience')

    class Meta:
        verbose_name = 'Doctor'
        verbose_name_plural = 'Doctors'

    def __str__(self):
        return f'Dr. {self.employee.full_name} - {self.speciality}'


class Administrator(models.Model):
    """Extended profile for administrators."""

    employee = models.OneToOneField(
        Employee,
        on_delete=models.CASCADE,
        related_name='administrator_profile',
        verbose_name='Employee',
        limit_choices_to={'user__role': 'administrator'},
    )
    system_access_rights = models.CharField(
        max_length=500,
        verbose_name='System access rights',
    )
    last_login_date = models.DateField(
        auto_now=True,
        verbose_name='Last login',
    )

    class Meta:
        verbose_name = 'Administrator'
        verbose_name_plural = 'Administrators'

    def __str__(self):
        return f'Admin: {self.employee.full_name}'
