from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from accounts.models import StudentProfile, InstructorProfile


@admin.register(get_user_model())
class CustomUserAdmin(UserAdmin):
    list_display = ('full_name', 'email', 'uuid',)
    list_filter = ('groups',)
    search_fields = ('full_name', 'email', 'uuid',)
    ordering = ('full_name',)
    fieldsets = (
        (None, {
            'fields': ('email', 'password')
        }),
        (_('Personal info'), {
            'fields': ('full_name',)
        }),
        (_('Permissions'), {
            'fields': ('is_staff', 'groups',),
        }),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'full_name', 'password1', 'password2'),
        }),
        (_('Permissions'), {
            'fields': ('is_staff', 'groups',),
        }),
    )

    def get_exclude(self, request, obj=None):
        excluded = super().get_exclude(request, obj) or []
        if not request.user.is_superuser:
            return excluded + ['is_active', 'is_superuser', 'user_permissions']
        return excluded


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('get_full_name', 'get_email', 'uuid',)
    search_fields = ('get_full_name', 'get_email', 'uuid',)

    def get_full_name(self, obj):
        return obj.user.full_name

    get_full_name.short_description = 'Full Name'
    get_full_name.admin_order_field = 'full_name'

    def get_email(self, obj):
        return obj.user.email

    get_email.short_description = 'Email'


@admin.register(StudentProfile)
class StudentProfileAdmin(UserProfileAdmin):
    pass


@admin.register(InstructorProfile)
class InstructorProfileAdmin(UserProfileAdmin):
    pass
