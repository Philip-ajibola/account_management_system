from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import AccountUser


# Register your models here.

@admin.register(AccountUser)
class AccountUserAdmin(UserAdmin):
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "password1", "password2", 'first_name', 'last_name'),
            },
        ),
    )