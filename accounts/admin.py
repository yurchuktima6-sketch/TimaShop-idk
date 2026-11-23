from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Profile


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'email', 'gamer_tag', 'phone', 'is_staff']
    fieldsets = UserAdmin.fieldsets + (
        ('Геймерські дані', {'fields': ('gamer_tag', 'phone')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Геймерські дані', {'fields': ('gamer_tag', 'phone')}),
    )


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'favorite_platform']
    search_fields = ['user__username', 'user__email', 'favorite_platform']