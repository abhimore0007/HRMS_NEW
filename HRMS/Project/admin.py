from django.contrib import admin
from .models import Department, Role, CustomUser
from django.contrib.auth.admin import UserAdmin

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('dept_name', 'description', 'status', 'created_at', 'updated_at')
    search_fields = ('dept_name',)
    list_filter = ('status',)
    ordering = ('dept_name',)

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('role_name', 'department', 'status', 'created_at', 'updated_at')
    search_fields = ('role_name',)
    list_filter = ('status', 'department')
    ordering = ('role_name',)

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'first_name', 'last_name', 'email', 'mobile', 'dept', 'role', 'date_of_joining')
    list_filter = ('dept', 'role', 'is_staff', 'is_superuser')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('username',)

    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('employee_id', 'mobile', 'dept', 'role', 'reporting_manager', 'date_of_joining')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('employee_id', 'mobile', 'dept', 'role', 'reporting_manager', 'date_of_joining')}),
    )
