from django.contrib import admin
from .models import CustomUser, Conversation, Message
from django.contrib.auth.admin import UserAdmin

class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('phone_number', 'role')}),
    )

# Register your models here.
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Conversation)
admin.site.register(Message)