from django.contrib import admin
from django.contrib.auth.models import User

from .models import UserProfile, UserConfig, UserPasswordHistoryMananger

# Register your models here.
admin.site.unregister(User)
admin.site.register((UserProfile, UserConfig))
admin.site.register(UserPasswordHistoryMananger)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'email', 'username', 'is_active']
    list_display_links = ['email', ]

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important Dates', {'fields': ('last_login', 'date_joined')}),
    )
