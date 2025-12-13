from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Company

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    # Fields shown in the list view
    list_display = ('username', 'email', 'role', 'is_staff', 'is_active')
    list_filter = ('role', 'is_staff', 'is_active')
    search_fields = ('username', 'email')

    # Fields shown in the form view
    fieldsets = UserAdmin.fieldsets + (
        ('Role Information', {'fields': ('role',)}),
    )

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'website')
    search_fields = ('name', 'owner__username')
    list_filter = ('name',)
