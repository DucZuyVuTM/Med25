from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Position, Employee, Doctor, Administrator

# Register your models here.
class DoctorInline(admin.StackedInline):
    model = Doctor
    extra = 0
    can_delete = False
    verbose_name_plural = 'Doctor information'


class AdministratorInline(admin.StackedInline):
    model = Administrator
    extra = 0
    can_delete = False
    verbose_name_plural = 'Administrator information'


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'salary', 'access_category')
    search_fields = ('title',)
    ordering = ('title',)


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = (
        'id', 
        'get_full_name',
        'position', 
        'get_phone',
        'employment_date', 
        'get_contract_end',
        'manager'
    )
    list_filter = ('position', 'employment_date')
    search_fields = ('user__first_name', 'user__last_name', 'user__phone')
    ordering = ('user__first_name', 'user__last_name')
    autocomplete_fields = ('position', 'manager')
    inlines = [DoctorInline, AdministratorInline]
    fieldsets = (
        ('Personal information', {
            'fields': ('user',)
        }),
        ('Work information', {
            'fields': ('position', 'manager', 'employment_date', 'contract_end_date')
        }),
    )

    @admin.display(description='Full name')
    def get_full_name(self, obj):
        return obj.user.full_name

    @admin.display(description='Phone')
    def get_phone(self, obj):
        return obj.user.phone

    @admin.display(description='Contract end')
    def get_contract_end(self, obj):
        return obj.contract_end_date


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_full_name', 'speciality', 'get_phone')
    search_fields = ('employee__user__first_name', 'employee__user__last_name', 'employee__user__phone', 'speciality')
    list_filter = ('speciality',)
    autocomplete_fields = ('employee',)

    @admin.display(description='Full name')
    def get_full_name(self, obj):
        return obj.employee.user.full_name

    @admin.display(description='Phone')
    def get_phone(self, obj):
        return obj.employee.user.phone


@admin.register(Administrator)
class AdministratorAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_full_name', 'system_access_rights', 'last_login_date')
    search_fields = ('user__first_name', 'user__last_name', 'user__phone')
    list_filter = ('last_login_date',)
    autocomplete_fields = ('employee',)
    
    @admin.display(description='Full name')
    def get_full_name(self, obj):
        return obj.employee.user.get_full_name()


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'phone', 'role', 'is_staff')
    list_filter = ('role', 'is_staff', 'is_active')
    search_fields = ('username', 'email', 'first_name', 'last_name', 'phone')

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Med25 Info', {'fields': ('patronymic', 'phone', 'address', 'role')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'email', 'first_name', 'last_name', 'patronymic', 'phone', 'address', 'role'),
        }),
    )

    ordering = ('first_name', 'last_name')
