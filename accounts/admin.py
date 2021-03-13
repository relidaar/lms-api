from django.contrib import admin

from accounts.models import CustomUser


class UserAdmin(admin.ModelAdmin):
    """Represent user model in the admin panel."""
    list_filter = ('role',)
    list_display = ('full_name', 'email', 'role',)


admin.site.register(CustomUser, UserAdmin)
