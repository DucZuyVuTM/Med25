from django.contrib import admin
from .models import Email, Message

# Register your models here.
class MessageInline(admin.TabularInline):
    model = Message
    extra = 0
    readonly_fields = ('send_date', 'send_time', 'sender_type')
    fields = ('sender_type', 'content', 'send_date', 'send_time')
    verbose_name_plural = 'Message'
    ordering = ('send_date', 'send_time')


@admin.register(Email)
class EmailAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'administrator', 'patient',
        'status', 'message_count'
    )
    search_fields = (
        'patient__surname', 'patient__name',
        'administrator__employee__surname',
    )
    list_filter = ('status', 'administrator')
    ordering = ('-id',)
    inlines = [MessageInline]

    def message_count(self, obj):
        return obj.messages.count()
    message_count.short_description = 'Message amount'


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_thread', 'sender_type', 'send_date', 'send_time', 'content_preview')
    search_fields = ('content', 'email__patient__surname')
    list_filter = ('sender_type', 'send_date')
    ordering = ('-send_date', '-send_time')

    def get_thread(self, obj):
        return f'Message #{obj.email.pk}'
    get_thread.short_description = 'Message thread'

    def content_preview(self, obj):
        return obj.content[:60] + '...' if len(obj.content) > 60 else obj.content
    content_preview.short_description = 'Content'
