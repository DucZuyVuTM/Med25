from django.db import models
from accounts.models import CustomUser

# Create your models here.
class MedicalCard(models.Model):
    """Patient's medical records - a one-to-one relationship with the Patient."""

    BLOOD_GROUP_CHOICES = [
        ('A+', 'A+'), ('A-', 'A-'),
        ('B+', 'B+'), ('B-', 'B-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'),
        ('O+', 'O+'), ('O-', 'O-'),
    ]

    patient = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='medical_card',
        verbose_name='Patient',
        limit_choices_to={'role': 'patient'},
    )
    allergy_info = models.TextField(verbose_name='Allergy information')
    blood_group = models.CharField(max_length=5, choices=BLOOD_GROUP_CHOICES, verbose_name='Blood group')
    current_medication = models.TextField(verbose_name='Medications currently being used')
    date_of_update = models.DateField(auto_now=True, verbose_name='Date updated')

    class Meta:
        verbose_name = 'Medical record'
        verbose_name_plural = 'Medical records'

    def __str__(self):
        return f'Medical record of {self.patient.full_name}'


class MedicalHistory(models.Model):
    """Medical history - the patient's past illnesses."""

    medical_card = models.ForeignKey(
        MedicalCard,
        on_delete=models.CASCADE,
        related_name='history_entries',
        verbose_name='Medical record',
    )
    disease_name = models.CharField(max_length=50, verbose_name='Name of the disease')
    treatment_date = models.DateField(verbose_name='Treatment date')

    class Meta:
        verbose_name = 'Medical history'
        verbose_name_plural = 'Medical histories'
        ordering = ['-treatment_date']

    def __str__(self):
        return f'{self.disease_name} ({self.treatment_date})'


class Diagnosis(models.Model):
    """A diagnosis was made for the patient."""

    medical_card = models.ForeignKey(
        MedicalCard,
        on_delete=models.CASCADE,
        related_name='diagnoses',
        verbose_name='Medical record',
    )
    diagnosis_content = models.TextField(verbose_name='Diagnostic content')
    diagnosis_date = models.DateField(verbose_name='Date of diagnosis')

    class Meta:
        verbose_name = 'Diagnosis'
        verbose_name_plural = 'Diagnoses'
        ordering = ['-diagnosis_date']

    def __str__(self):
        return f'Diagnosis {self.diagnosis_date} - {self.medical_card.patient.full_name}'


class Analysis(models.Model):
    """The patient's analysis results."""

    medical_card = models.ForeignKey(
        MedicalCard,
        on_delete=models.CASCADE,
        related_name='analyses',
        verbose_name='Medical record',
    )
    list_of_analysis_samples = models.TextField(verbose_name='List of analysis samples')
    analysis_result = models.TextField(verbose_name='Analysis result')
    analysis_date = models.DateField(verbose_name='Analysis date')

    class Meta:
        verbose_name = 'Analysis'
        verbose_name_plural = 'Analyses'
        ordering = ['-analysis_date']

    def __str__(self):
        return f'Analysis {self.analysis_date} - {self.medical_card.patient.full_name}'
