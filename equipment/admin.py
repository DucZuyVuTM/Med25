from django.contrib import admin
from .models import ClinicEquipmentCategory, ClinicEquipment

# Register your models here.
class ClinicEquipmentInline(admin.TabularInline):
    model = ClinicEquipment
    extra = 0
    show_change_link = True
    fields = ('name', 'price', 'warranty_period')
    verbose_name_plural = 'Clinic Equipment'


@admin.register(ClinicEquipmentCategory)
class ClinicEquipmentCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'description_preview', 'equipment_count')
    search_fields = ('description',)
    inlines = [ClinicEquipmentInline]

    def description_preview(self, obj):
        return obj.description[:60] + '...' if len(obj.description) > 60 else obj.description
    description_preview.short_description = 'Description'

    def equipment_count(self, obj):
        return obj.equipment_items.count()
    equipment_count.short_description = 'Equipment amount'


@admin.register(ClinicEquipment)
class ClinicEquipmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'price', 'warranty_period')
    search_fields = ('name', 'certificate')
    list_filter = ('category', 'warranty_period')
    ordering = ('name',)
    autocomplete_fields = ('category',)
    fieldsets = (
        ('Equipment information', {
            'fields': ('category', 'name', 'price')
        }),
        ('Detail', {
            'fields': ('instruction', 'certificate', 'warranty_period')
        }),
    )
