from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _


@admin.register(get_user_model())
class CustomUserAdmin(UserAdmin):
    list_display = ('full_name', 'email', 'uuid',)
    search_fields = ('full_name', 'email', 'uuid',)
    ordering = ('email',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('full_name',)}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
    )

    def get_exclude(self, request, obj=None):
        excluded = super().get_exclude(request, obj) or []
        if not request.user.is_superuser:
            excluded += ('is_active', 'is_superuser', 'user_permissions',)
        return excluded
