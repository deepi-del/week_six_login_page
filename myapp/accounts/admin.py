from django.contrib import admin
from .models import CustomUser, AdminProfile
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

class CustomUserAdmin(BaseUserAdmin):
    # Specify which fields to display in the list view
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_active', 'is_staff')
    list_filter = ('is_active', 'is_staff')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('username',)
    
    # Fields to use for creating and editing users
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),  
        (_('Important dates'), {'fields': ('last_login',)}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'is_active', 'is_staff')}
        ),
    )

# Register CustomUser with the customized admin class
admin.site.register(CustomUser, CustomUserAdmin)

class AdminProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'department', 'is_superuser')
    search_fields = ('user__username', 'department')

# Register AdminProfile with its own admin class
admin.site.register(AdminProfile, AdminProfileAdmin)
