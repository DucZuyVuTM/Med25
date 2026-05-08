from django.contrib import admin

from .models import MedicalCard, MedicalHistory, Diagnosis, Analysis

# Register your models here.
class MedicalHistoryInline(admin.TabularInline):
    model = MedicalHistory
    extra = 1
    verbose_name_plural = 'Medical history'


class DiagnosisInline(admin.TabularInline):
    model = Diagnosis
    extra = 1
    verbose_name_plural = 'Diagnosis'


class AnalysisInline(admin.TabularInline):
    model = Analysis
    extra = 1
    verbose_name_plural = 'Analysis'


class MedicalCardInline(admin.StackedInline):
    model = MedicalCard
    extra = 0
    can_delete = False
    verbose_name_plural = 'Medical Document'
    show_change_link = True


@admin.register(MedicalCard)
class MedicalCardAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'get_patient_name', 'blood_group',
        'date_of_update'
    )
    search_fields = ('patient__surname', 'patient__name', 'patient__phone')
    list_filter = ('blood_group', 'date_of_update')
    inlines = [MedicalHistoryInline, DiagnosisInline, AnalysisInline]
    fieldsets = (
        ('Patient', {
            'fields': ('patient',)
        }),
        ('Medical information', {
            'fields': ('blood_group', 'allergy_info', 'current_medication', 'date_of_update')
        }),
    )

    def get_patient_name(self, obj):
        return obj.patient.full_name
    get_patient_name.short_description = 'Patient'


@admin.register(MedicalHistory)
class MedicalHistoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_patient', 'disease_name', 'treatment_date')
    search_fields = ('disease_name', 'medical_card__patient__surname')
    list_filter = ('treatment_date',)
    ordering = ('-treatment_date',)

    def get_patient(self, obj):
        return obj.medical_card.patient.full_name
    get_patient.short_description = 'Patient'


@admin.register(Diagnosis)
class DiagnosisAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_patient', 'diagnosis_content', 'diagnosis_date')
    search_fields = ('diagnosis_content', 'medical_card__patient__surname')
    list_filter = ('diagnosis_date',)
    ordering = ('-diagnosis_date',)

    def get_patient(self, obj):
        return obj.medical_card.patient.full_name
    get_patient.short_description = 'Patient'


@admin.register(Analysis)
class AnalysisAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_patient', 'analysis_date')
    search_fields = ('medical_card__patient__surname', 'list_of_analysis_samples')
    list_filter = ('analysis_date',)
    ordering = ('-analysis_date',)

    def get_patient(self, obj):
        return obj.medical_card.patient.full_name
    get_patient.short_description = 'Patient'
