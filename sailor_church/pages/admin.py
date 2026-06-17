from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from phonenumber_field.widgets import PhoneNumberPrefixWidget
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser

# Register your models here.
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser

    list_display = ['email', 'first_name', 'surname', 'phone_number', 'is_staff']
    ordering = ['email']
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'surname', 'phone_number')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('collapse',),
            'fields': ('email', 'first_name', 'surname', 'phone_number', 'password'),
        }),
    )

admin.site.register(CustomUser, CustomUserAdmin)