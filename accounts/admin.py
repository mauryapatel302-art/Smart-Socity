from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'email', 'role', 'phone', 'flat']
    fieldsets = UserAdmin.fieldsets + (
        ('Society Info', {'fields': ('role', 'phone', 'flat')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)
