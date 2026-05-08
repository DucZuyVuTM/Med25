from django.contrib import admin
from .models import Document

# Register your models here.
@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('id', 'administrator', 'formation_date', 'content_preview')
    search_fields = ('content', 'administrator__employee__first_name')
    list_filter = ('formation_date', 'administrator')
    ordering = ('-formation_date',)
    readonly_fields = ('formation_date',)

    def content_preview(self, obj):
        return obj.content[:80] + '...' if len(obj.content) > 80 else obj.content
    content_preview.short_description = 'Description'
