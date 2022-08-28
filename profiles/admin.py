from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Profile

class CustomUserAdmin(UserAdmin):
    """Custom Admin Panel Users Model"""
    model = User
    fieldsets = (*UserAdmin.fieldsets, ("Email Verification", {"fields": ("email_verified",)}))
    list_display = ("username", "email", 'email_verified')

admin.site.register(Profile)
admin.site.register(User, CustomUserAdmin)